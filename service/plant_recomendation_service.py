from flask import Flask, request, jsonify
import os
import pickle
from google.cloud import storage
import uuid
from AI.service.predict_plants import PredictPlants


class PlantRecomendationService:
    def __init__(self):
        pass

    app = Flask(__name__)

    def predict(self, humidity, temperature):

        predict = PredictPlants.predict(humidity, temperature)

        # Return the prediction as JSON response
        response = predict
        return jsonify(response), 200

    def get_plant_recomendation(self):
        response_data = {
            "error": False,
            "message": "Lahan fetched successfully",
            "data": "OK",
        }
        return jsonify(response_data), 200
