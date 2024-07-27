import numpy as np
from tensorflow import keras

def process_ecg_data(ecg_data):
    # Process ECG data and calculate BPM
    return np.random.randint(60, 100)  # Placeholder: returns random BPM

def predict_anomaly(ecg_data):
    # Load the saved model
    model = keras.models.load_model('../../saved_model/final_model.keras')
    
    # Preprocess the data
    ecg_data = np.array(ecg_data).reshape(1, -1, 1)
    
    # Make prediction
    prediction = model.predict(ecg_data)
    
    # Interpret the prediction
    classes = ['N', 'S', 'V', 'F', 'Q']
    predicted_class = classes[np.argmax(prediction)]
    
    # Return True if anomaly detected, False otherwise
    return predicted_class != 'N'