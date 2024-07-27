import numpy as np

# These functions are placeholders. In a real application, you would connect to a real database.

def save_ecg_data(data):
    # Save ECG data to database
    pass

def get_latest_ecg_data():
    # Get latest ECG data from database
    return np.random.randn(100)  # Placeholder: returns random data

def get_ecg_users():
    # Get list of ECG users from database
    return ["User1", "User2", "User3"]

def get_user_ecg_data(username):
    # Get ECG data for a specific user
    return {
        "ecg_data": np.random.randn(100),
        "bpm": np.random.randint(60, 100),
        "status": np.random.choice(["Normal", "Low", "High"])
    }