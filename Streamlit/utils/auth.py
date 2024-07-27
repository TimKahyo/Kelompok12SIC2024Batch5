import streamlit as st

# This is a mock authentication function. In a real application, you would use a secure authentication system.
def login(username, password, role):
    # Mock user database
    users = {
        "user1": {"password": "pass1", "role": "User ECG"},
        "user2": {"password": "pass2", "role": "User Emergence"}
    }
    
    if username in users and users[username]["password"] == password and users[username]["role"] == role:
        return {"username": username, "role": role}
    return None