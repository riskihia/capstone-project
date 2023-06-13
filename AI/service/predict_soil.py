from flask import Flask, render_template, request,jsonify
import os
import pickle
from google.cloud import storage
import uuid
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image


class PredictSoil:
    
    def __init__(self):
        pass

    def predict(image):
    
        # Mendapatkan lokasi direktori saat ini
        current_dir = os.getcwd()

        # Mendapatkan jalur ke file model kmeans
        cnn_model_path = os.path.join(
            current_dir, 'AI', 'assets', 'model_tanah.h5')

        # Memuat model CNN dari file
        # load json dan buat model
        json_file = open(cnn_model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights menjadi model baru
        loaded_model.load_weights("model_tanah.h5")
        
         # predicting images
        # file = request.files['image']
        
        img = load_img(image, target_size=(150, 150))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        prediction = loaded_model.predict(images, batch_size=10)

        # Mendapatkan indeks maksimum dari hasil prediksi
        predicted_label_index = np.argmax(prediction)
        
        # Daftar label yang sesuai dengan indeks prediksi
        labels = ['Tanah_Aluvial','Tanah_Geluh', 'Tanah Laterit','Tanah Liat']

        # Mendapatkan label prediksi
        predicted_label = labels[predicted_label_index]

        print(img)
        print(prediction)
        print(f'Hasil prediksi tanah : {predicted_label}')
        
                

        # Return the prediction as JSON response
        response = {
            'prediction': predicted_label.tolist()
        }
        return response


