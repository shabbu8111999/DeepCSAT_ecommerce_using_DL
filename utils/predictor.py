import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


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

        # Same value used in training
        self.max_length = 120

    def predict(self, remark, response_time, survey_delay,
                issue_hour, issue_day, issue_month):

        # ---------- TEXT PROCESSING ----------

        sequence = self.tokenizer.texts_to_sequences([remark])

        padded_sequence = pad_sequences(
            sequence,
            maxlen=self.max_length,
            padding="post"
        )

        # ---------- STRUCTURED FEATURES ----------

        structured_features = np.array([[
            response_time,
            survey_delay,
            issue_hour,
            issue_day,
            issue_month
        ]])

        scaled_features = self.scaler.transform(structured_features)

        # ---------- MODEL PREDICTION ----------

        prediction = self.model.predict([padded_sequence, scaled_features])

        predicted_class = np.argmax(prediction)

        # Convert back to original CSAT scale (1–5)

        csat_score = int(predicted_class) + 1

        return csat_score