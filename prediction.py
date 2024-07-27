import streamlit as st
import pymongo
from urllib.parse import quote_plus
import numpy as np
import tensorflow as tf

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
model_path = 'E:/project_e/model/model.keras'
try:
    model = tf.keras.models.load_model(model_path)
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")

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

# Streamlit UI
st.title("ECG Heartbeat Anomaly Detection")

# Retrieve data from MongoDB
def get_latest_data():
    latest_record = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
    if latest_record:
        return np.array(latest_record['data']).astype(np.float32)
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

# Button to trigger prediction
if st.button('Get Latest ECG Data and Predict'):
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
