from flask import Flask, request, jsonify
import os
import pickle
from google.cloud import storage
import uuid
from AI.service.predict_soil import PredictSoil


class SoilPredictionService:
    def __init__(self):
        pass

    app = Flask(__name__)

    def predict(self, image):

        predict = PredictSoil.predict(image)

        # Return the prediction as JSON response
        response = predict
        return jsonify(response), 200

    def get_soil_class(self):
        response_data = {
            "error": False,
            "message": "Jenis tanah ok",
            "data": "OK",
        }
        return jsonify(response_data), 200
