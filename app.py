import logging

from flask import Flask, render_template, request, jsonify

from utils.predictor import CSATPredictor


# configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("DeepCSAT")


app = Flask(__name__)


# load model once
predictor = CSATPredictor()


@app.route("/")
def home():

    # render main page
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        # get inputs
        remark = data["remark"]

        response_time = float(data["response_time"])
        survey_delay = float(data["survey_delay"])

        issue_hour = int(data["issue_hour"])
        issue_day = int(data["issue_day"])
        issue_month = int(data["issue_month"])

        # run prediction
        csat_score, probabilities = predictor.predict(
            remark,
            response_time,
            survey_delay,
            issue_hour,
            issue_day,
            issue_month
        )

        return jsonify({

            "predicted_csat": csat_score,

            "probabilities": probabilities

        })

    except Exception as e:

        logger.error(str(e))

        return jsonify({

            "error": "Prediction failed"

        })


if __name__ == "__main__":

    # start flask server
    app.run(debug=True)