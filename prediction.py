import streamlit as st
import pymongo
from urllib.parse import quote_plus
import numpy as np
import tensorflow as tf
import keras
from PIL import Image
from io import BytesIO

# MongoDB credentials
username = quote_plus("adminmari")
password = quote_plus("mari@123")

# MongoDB connection URI
uri = f"mongodb+srv://{username}:{password}@mari.fmejyxn.mongodb.net/?retryWrites=true&w=majority&appName=Mari"

# Connect to MongoDB
client = pymongo.MongoClient(uri)
db = client['ECGDatabase']
collection = db['ECGData']

# Load the Keras model
model_path = 'model/model.h5'

model = keras.models.load_model(model_path)


# Definisikan label kelas dan anotasi
classes = ['N', 'S', 'V', 'F', 'Q']
annotations= {
    'N': {
        'annotations': ['Normal', 'Blok cabang berkas kiri/kanan', 'Escape atrium', 'Escape nodal'],
        'description': 'Detak jantung normal dan ketidakteraturan minor yang biasanya tidak menunjukkan masalah.'
    },
    'S': {
        'annotations': ['Prematur atrium', 'Prematur atrium abnormal', 'Prematur nodal', 'Prematur supra-ventrikel'],
        'description': 'Detak jantung prematur yang berasal dari bilik atas jantung, yang bisa tidak berbahaya tetapi kadang-kadang membutuhkan perhatian medis.'
    },
    'V': {
        'annotations': ['Kontraksi ventrikel prematur', 'Escape ventrikel'],
        'description': 'Detak jantung prematur yang berasal dari bilik bawah jantung, yang bisa lebih serius dan mungkin memerlukan perawatan.'
    },
    'F': {
        'annotations': ['Fusi ventrikel dan normal'],
        'description': 'Kombinasi detak jantung normal dan abnormal, yang mungkin menunjukkan masalah mendasar yang perlu evaluasi.'
    },
    'Q': {
        'annotations': ['Paced', 'Fusi paced dan normal', 'Tidak dapat diklasifikasikan'],
        'description': 'Detak jantung yang dipengaruhi oleh alat pacu jantung atau detak tidak teratur yang tidak masuk ke dalam kategori lain, sering diawasi oleh penyedia layanan kesehatan.'
    }
}

# def logo_to_base64(img):
#     buffered = BytesIO()
#     img.save(buffered, format="PNG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()
#     return img_str

# # Load the logo
# logo = Image.open('frontend/assets/logo.png')
# logo_base64 = logo_to_base64(logo)

# Display the logo and title side by side
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="flex: 1;">
            <img src="https://raw.githubusercontent.com/TimKahyo/Kelompok12SIC2024Batch5/main/frontend/assets/logo.png" style="width: 150px; height: auto;">
        </div>
        <div style="flex: 2; text-align: left;">
            <h1>
                <span style="color: #0036B9;">Mari:</span>
                <span style="color: #FFB923;">Sistem Pemantauan Kesehatan Jantung</span>
            </h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Retrieve data from MongoDB
def get_latest_data():
    latest_record = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
    if latest_record:
        return np.array(latest_record['ecg_data']).astype(np.float32)
    else:
        st.error("No data found in MongoDB.")
        return None

# Predict anomaly
def predict_anomaly(data):
    if data is not None:
        # Reshape data to match model input shape
        data = np.expand_dims(data, axis=0)  # Add batch dimension
        predictions = model.predict(data)
        predicted_class_index = np.argmax(predictions, axis=1)
        predicted_class_label = classes[predicted_class_index[0]]
        predicted_annotations = annotations[predicted_class_label]['annotations']
        predicted_description = annotations[predicted_class_label]['description']
        return predicted_class_label, predicted_annotations, predicted_description
    else:
        return None, None, None

# Custom CSS to style the button
st.markdown(
    """
    <style>
    .custom-button {
        color: #0036B9;
        border: 2px solid #FFB923;
        background-color: transparent;
        padding: 0.5em 1em;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: #0036B9;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Button to trigger prediction
if st.markdown('<button class="custom-button">Dapatkan Data EKG Terbaru dan Prediksi</button>', unsafe_allow_html=True):
    latest_data = get_latest_data()
    if latest_data is not None:
        st.write("Data EKG Terbaru Diperoleh dari MongoDB")
        st.write(latest_data)
        predicted_class, annotations, description = predict_anomaly(latest_data)
        if predicted_class:
            st.success(f"Kelas yang Diprediksi: {predicted_class}")
            st.write("Anotasi:")
            for annotation in annotations:
                st.write(f"- {annotation}")
            st.write(f"Deskripsi: {description}")
