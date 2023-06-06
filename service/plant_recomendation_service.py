from flask import Flask, request, jsonify
import os
import pickle
from google.cloud import storage
import uuid



class PlantRecomendationService:
    def __init__(self):
        pass

    app = Flask(__name__)
    

    def load_model_from_gcp(bucket_name, file_name):
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        model_bytes = blob.download_as_bytes()
        model = pickle.loads(model_bytes)
        return model
    
    # @app.route('/predict',methods=['POST'])
    def predict(model, data):

        # Perform prediction
        temperature = data[0]['temperature']
        humidity = data[0]['humidity']
        input_data = [[temperature, humidity]]
        prediction = model.predict(input_data)

        # Return the prediction as JSON response
        response = {
            'prediction': prediction.tolist()
        }
        return jsonify(response)

    def get_plant_recomendation():
        return jsonify({'plant_recomendation': 'plant_recomendation'})
    if __name__ == '__main__':
        app.run()
