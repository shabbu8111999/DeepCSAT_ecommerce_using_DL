import numpy as np
import pickle
import re

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


class CSATPredictor:

    def __init__(self):

        # load trained model
        self.model = load_model("artifacts/csat_lstm_model.h5")

        # load tokenizer
        with open("artifacts/tokenizer.pkl", "rb") as f:
            self.tokenizer = pickle.load(f)

        # load scaler
        with open("artifacts/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

        # max length used during training
        self.max_length = 120


    def preprocess_text(self, text):

        # convert text to lowercase
        text = text.lower()

        # remove special characters
        text = re.sub(r"[^a-z\s]", " ", text)

        # remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        # remove stopwords
        words = text.split()

        filtered_words = [
            word for word in words
            if word not in ENGLISH_STOP_WORDS
        ]

        cleaned_text = " ".join(filtered_words)

        return cleaned_text


    def predict(self,
                remark,
                response_time,
                survey_delay,
                issue_hour,
                issue_day,
                issue_month):

        # clean remark text
        cleaned_remark = self.preprocess_text(remark)

        # convert text to sequence
        sequence = self.tokenizer.texts_to_sequences([cleaned_remark])

        # pad sequence
        padded_sequence = pad_sequences(
            sequence,
            maxlen=self.max_length,
            padding="post"
        )

        # structured features
        structured_features = np.array([[
            response_time,
            survey_delay,
            issue_hour,
            issue_day,
            issue_month
        ]])

        # scale numeric features
        scaled_features = self.scaler.transform(structured_features)

        # model prediction
        prediction = self.model.predict(
            [padded_sequence, scaled_features]
        )

        # predicted class
        predicted_class = np.argmax(prediction)

        # convert class back to CSAT scale
        csat_score = int(predicted_class) + 1

        # probability for each class
        probabilities = prediction[0].tolist()

        return csat_score, probabilities