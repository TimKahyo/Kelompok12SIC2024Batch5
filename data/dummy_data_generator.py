import numpy as np
import pymongo
from urllib.parse import quote_plus

# Create a single sample with 186 timesteps, each having 1 feature
single_sample = np.random.rand(186, 1).astype(np.float32).tolist()

# Ensuring the single sample has 186 timesteps
single_sample_example = np.resize(single_sample, (186, 1)).tolist()

# URL-encode username and password
username = quote_plus("adminmari")
password = quote_plus("mari@123")

# MongoDB connection details
uri = f"mongodb+srv://{username}:{password}@mari.fmejyxn.mongodb.net/?retryWrites=true&w=majority&appName=Mari"
client = pymongo.MongoClient(uri)

# Select the database and collection
db = client['ECGDatabase']
collection = db['ECGData']

# Insert the dummy data
document = {
    "ecg_data": single_sample_example
}

result = collection.insert_one(document)
print(f"Inserted document ID: {result.inserted_id}")
