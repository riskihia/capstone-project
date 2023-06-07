from flask import Flask, request, jsonify
import os
import pickle
from google.cloud import storage
import uuid


class PlantRecomendationService:
    def __init__(self):
        pass

    app = Flask(__name__)

    # @app.route('/predict', methods=['POST'])
    def predict(self, humidity, temperature):

        # Mendapatkan lokasi direktori saat ini
        current_dir = os.getcwd()

        # Mendapatkan jalur ke file model kmeans
        kmeans_model_path = os.path.join(
            current_dir, 'assets', 'machine_learning', 'model_kmeans.pickle')

        # Memuat model kmeans dari file
        with open(kmeans_model_path, 'rb') as file:
            kmeans_model = pickle.load(file)

        # Membuat input data untuk prediksi
        input_data = [[temperature, humidity]]
        cluster_predict = kmeans_model.predict(input_data)

        # Mengambil nilai prediksi klaster
        cluster = cluster_predict[0]

        # Menambahkan label cluster kedalam var input untuk proses
        input_data[0].append(cluster)

        filename_model_cluster = f'model_cluster_{cluster}.pickle'

        # Mendapatkan jalur ke file model klasifikasi klaster
        cluster_model_path = os.path.join(
            current_dir, 'assets', 'machine_learning', filename_model_cluster)

        with open(cluster_model_path, 'rb') as file:
            cluster_model = pickle.load(file)

        prediction = cluster_model.predict(input_data)

        # Return the prediction as JSON response
        response = {
            'prediction': prediction.tolist()
        }
        return jsonify(response)

    def get_plant_recomendation(self):
        response_data = {
            "error": False,
            "message": "Lahan fetched successfully",
            "data": "OK",
        }
        return jsonify(response_data), 200
