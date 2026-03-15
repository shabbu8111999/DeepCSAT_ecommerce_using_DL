import numpy as np
import pickle
import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


class CSATPredictor:

    def __init__(self):

        # Load trained model
        self.model = load_model("artifacts/csat_lstm_model.h5")

        # Load tokenizer
        with open("artifacts/tokenizer.pkl", "rb") as f:
            self.tokenizer = pickle.load(f)

        # Load scaler
        with open("artifacts/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

        # Same sequence length used during training
        self.max_length = 120

    
    # TEXT PREPROCESSING FUNCTION
    def preprocess_text(self, text):

        # Convert to lowercase
        text = text.lower()

        # Remove numbers and special characters
        text = re.sub(r"[^a-z\s]", " ", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Remove stopwords
        words = text.split()

        filtered_words = [
            word for word in words
            if word not in ENGLISH_STOP_WORDS
        ]

        cleaned_text = " ".join(filtered_words)

        return cleaned_text

    
    # PREDICTION FUNCTION
    def predict(self, remark,
                response_time,
                survey_delay,
                issue_hour,
                issue_day,
                issue_month):

        # Apply text preprocessing
        cleaned_remark = self.preprocess_text(remark)

        # Convert text → sequence
        sequence = self.tokenizer.texts_to_sequences([cleaned_remark])

        # Pad sequence
        padded_sequence = pad_sequences(
            sequence,
            maxlen=self.max_length,
            padding="post"
        )

        # Structured numerical features
        structured_features = np.array([[
            response_time,
            survey_delay,
            issue_hour,
            issue_day,
            issue_month
        ]])

        # Scale features
        scaled_features = self.scaler.transform(structured_features)

        # Model prediction
        prediction = self.model.predict(
            [padded_sequence, scaled_features]
        )

        predicted_class = np.argmax(prediction)

        # Convert back to original CSAT scale (1–5)
        csat_score = int(predicted_class) + 1

        return csat_score