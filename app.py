import os
import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import urllib.parse
import numpy as np

# Memuat variabel dari file .env
load_dotenv()

# Mengatur logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Mendapatkan username, password, dan nama database dari variabel lingkungan
MONGO_USERNAME = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
MONGO_PASSWORD = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_BASE_URI = os.getenv("MONGO_BASE_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

# Membentuk URI MongoDB yang lengkap
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_BASE_URI}"

try:
    # Konfigurasi koneksi MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]  # Menggunakan database dari variabel lingkungan
    logging.info("Successfully connected to the database")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
    raise e

# Koleksi pengguna
ecg_data_collection = db["ecg_data"]  # Menggunakan koleksi 'ecg_data'


# array list dataEcg
dataEcg = []

@app.route("/ecg", methods=["POST"])
def ecg_data():
    try:
        data = request.json
        ecg_value = data.get("value")
        ecg_data_collection.insert_one(
            {"value": ecg_value}
        )  # Menambahkan nilai ECG ke dalam koleksi
        logging.info(f"Received ECG value: {ecg_value}")
        return jsonify({"message": "Data received", "ecg_value": ecg_value}), 200
    except Exception as e:
        logging.error(f"Error in /ecg POST: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/ecg", methods=["GET"])
def get_ecg_data():
    try:
        count = request.args.get("count", default=10, type=int)
        ecg_data_cursor = ecg_data_collection.find().sort("_id", -1).limit(count)
        recent_ecg_data = [doc["value"] for doc in ecg_data_cursor]

        # Menghitung rata-rata bergerak
        moving_average = (
            sum(recent_ecg_data) / len(recent_ecg_data) if recent_ecg_data else 0
        )

        return (
            jsonify(
                {
                    "message": f"Last {count} ECG data and their moving average",
                    "ecg_data": recent_ecg_data,
                    "moving_average": moving_average,
                }
            ),
            200,
        )
    except Exception as e:
        logging.error(f"Error in /ecg GET: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/ecg/all", methods=["GET"])
def get_all_ecg_dataMv():
    try:
        ecg_data_cursor = ecg_data_collection.find()
        all_ecg_data = [{"dataValue": doc["dataValue"]} for doc in ecg_data_cursor]

        return jsonify({"message": "All ECG data", "ecg_data": all_ecg_data}), 200
    except Exception as e:
        logging.error(f"Error in /ecg/all GET: {e}")
        return jsonify({"error": str(e)}), 500


# @app.route("/ecg/init", methods=["POST"])
# def init_ecg_data():
#     values = np.random.rand(186, 1).astype(np.float32)
#     initial_values = np.resize(values, (186, 1))
#     ecg_data_collection.insert_one(
#         {"dataValue": initial_values}
#     )  # Menambahkan nilai awal sebagai satu dokumen
#     logging.info(f"Initial ECG values added: {initial_values}")
#     return (
#         jsonify({"message": "Initial data added", "initial_values": initial_values}),
#         200,
#     )





# @app.route("/ecg/add", methods=["POST"])
# def add_ecg_data():
#     try:
#         data = request.json
#         ecg_values = data.get("dataValue")
#         ecg_data_collection.insert_one(
#             {"dataValue": ecg_values}
#         )  # <- Menambahkan nilai baru sebagai satu dokumen
#         logging.info(f"New ECG values added: {ecg_values}")
#         return jsonify({"message": "Data added", "dataValue": ecg_values}), 200
#     except Exception as e:
#         logging.error(f"Error in /ecg/add POST: {e}")
#         return jsonify({"error": str(e)}), 500



@app.route("/ecg/init", methods=["POST"])
def init_ecg_data():
    try:
        values = np.random.rand(186, 1).astype(np.float32)
        initial_values = values.tolist()  # Konversi numpy array ke list
        ecg_data_collection.insert_one(
            {"dataValue": initial_values}
        )  # Menambahkan nilai awal sebagai satu dokumen
        logging.info(f"Initial ECG values added: {initial_values}")
        return (
            jsonify({"message": "Initial data added", "initial_values": initial_values}),
            200,
        )
    except Exception as e:
        logging.error(f"Error in /ecg/init POST: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/ecg/add", methods=["POST"])
def add_ecg_data():
    global dataEcg
    try:
        data = request.json
        ecg_values = data.get("dataValue") 
        ecg_values = ecg_values / 4095.0

        
        ecg_values = [ecg_values]
        dataEcg.append(ecg_values)
        
        if len(dataEcg) == 3 :
            ecg_data_collection.insert_one(
                {"dataValue": dataEcg}
            )  # Menambahkan nilai baru sebagai satu dokumen
            dataEcg = []
    
        logging.info(f"New ECG values added: {dataEcg}")
        return jsonify({"message": "Data added", "dataValue": dataEcg}), 200
    except Exception as e:
        logging.error(f"Error in /ecg/add POST: {e}")
        return jsonify({"error": str(e)}), 500
    


# Get system
@app.route("/ecg/get_latestEcg", methods=["GET"])
def get_latest_ecg_data():
    try:
        # Mengambil dokumen terbaru
        latest_ecg_data = ecg_data_collection.find_one(sort=[("_id", -1)])

        if latest_ecg_data:
            logging.info(f"Retrieved latest ECG data: {latest_ecg_data['dataValue']}")
            return (
                jsonify(
                    {
                        "message": "Latest ECG data retrieved",
                        "dataValue": latest_ecg_data["dataValue"],
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "No ECG data found"}), 404
    except Exception as e:
        logging.error(f"Error in /ecg/get_latest GET: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/ecg/get_allData", methods=["GET"])
def get_all_ecg_data():
    try:
        # Mengambil semua dokumen dari koleksi
        ecg_data_cursor = ecg_data_collection.find()
        all_ecg_data = [{"dataValue": doc["dataValue"]} for doc in ecg_data_cursor]

        if all_ecg_data:
            logging.info(f"Retrieved all ECG data.")
            return (
                jsonify({"message": "All ECG data retrieved", "data": all_ecg_data}),
                200,
            )
        else:
            return jsonify({"message": "No ECG data found"}), 404
    except Exception as e:
        logging.error(f"Error in /ecg/get_all GET: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
