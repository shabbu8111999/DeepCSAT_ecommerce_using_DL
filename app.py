import logging
from flask import Flask, render_template, request, jsonify
from utils.predictor import CSATPredictor



# LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("DeepCSAT")


# INITIALIZE FLASK
app = Flask(__name__)


# LOAD MODEL ONCE
try:
    logger.info("Loading CSAT prediction model...")

    predictor = CSATPredictor()

    logger.info("Model loaded successfully")

except Exception as e:

    logger.error(f"Error loading model: {str(e)}")
    predictor = None


# HOME ROUTE
@app.route("/")
def home():
    """
    Render the prediction interface.
    """
    return render_template("index.html")


# PREDICTION API
@app.route("/predict", methods=["POST"])
def predict():

    if predictor is None:
        return jsonify({
            "error": "Model is not available"
        }), 500

    try:

        data = request.get_json()

        # -------- Input Validation --------

        remark = data.get("remark", "").strip()

        if remark == "":
            return jsonify({
                "error": "Customer remark cannot be empty"
            }), 400

        response_time = float(data.get("response_time"))
        survey_delay = float(data.get("survey_delay"))
        issue_hour = int(data.get("issue_hour"))
        issue_day = int(data.get("issue_day"))
        issue_month = int(data.get("issue_month"))

        # -------- Model Prediction --------

        prediction = predictor.predict(
            remark,
            response_time,
            survey_delay,
            issue_hour,
            issue_day,
            issue_month
        )

        logger.info(f"Prediction successful: {prediction}")

        return jsonify({
            "predicted_csat": prediction
        })

    except ValueError:

        return jsonify({
            "error": "Invalid numerical input"
        }), 400

    except Exception as e:

        logger.error(f"Prediction error: {str(e)}")

        return jsonify({
            "error": "Internal server error"
        }), 500


# RUN SERVER
if __name__ == "__main__":

    logger.info("Starting DeepCSAT Flask server")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )