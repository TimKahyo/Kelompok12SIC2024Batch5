def check_password(username, password, role):
    if role == "ECG User":
        return username == "user" and password == "password"
    elif role == "Emergency Personnel":
        return username == "emergency" and password == "password"
    return False