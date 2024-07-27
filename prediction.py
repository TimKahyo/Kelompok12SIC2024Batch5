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

# Define class labels and annotations
classes = ['N', 'S', 'V', 'F', 'Q']
annotations = {
    'N': {
        'annotations': ['Normal', 'Left/Right bundle branch block', 'Atrial escape', 'Nodal escape'],
        'description': 'Normal heartbeats and minor irregularities that usually do not indicate a problem.'
    },
    'S': {
        'annotations': ['Atrial premature', 'Aberrant atrial premature', 'Nodal premature', 'Supra-ventricular premature'],
        'description': 'Premature heartbeats originating from the upper chambers of the heart, which can be harmless but sometimes need medical attention.'
    },
    'V': {
        'annotations': ['Premature ventricular contraction', 'Ventricular escape'],
        'description': 'Premature heartbeats originating from the lower chambers of the heart, which can be more serious and may require treatment.'
    },
    'F': {
        'annotations': ['Fusion of ventricular and normal'],
        'description': 'A combination of normal and abnormal heartbeats, which might indicate an underlying issue needing evaluation.'
    },
    'Q': {
        'annotations': ['Paced', 'Fusion of paced and normal', 'Unclassifiable'],
        'description': 'Heartbeats influenced by a pacemaker or irregular beats that do not fit into other categories, often monitored by healthcare providers.'
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
if st.markdown('<button class="custom-button">Get Latest ECG Data and Predict</button>', unsafe_allow_html=True):
    latest_data = get_latest_data()
    if latest_data is not None:
        st.write("Latest ECG Data Retrieved from MongoDB")
        st.write(latest_data)
        predicted_class, annotations, description = predict_anomaly(latest_data)
        if predicted_class:
            st.success(f"Predicted Class: {predicted_class}")
            st.write("Annotations:")
            for annotation in annotations:
                st.write(f"- {annotation}")
            st.write(f"Description: {description}")