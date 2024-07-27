import os
import logging
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import urllib.parse

# Memuat variabel dari file .env
load_dotenv()

# Mengatur logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Mendapatkan username, password, dan nama database dari variabel lingkungan
MONGO_USERNAME = urllib.parse.quote_plus(os.getenv('MONGO_USERNAME'))
MONGO_PASSWORD = urllib.parse.quote_plus(os.getenv('MONGO_PASSWORD'))
MONGO_BASE_URI = os.getenv('MONGO_BASE_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')

# Membentuk URI MongoDB yang lengkap
MONGO_URI = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_BASE_URI}'

try:
    # Konfigurasi koneksi MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]  # Menggunakan database dari variabel lingkungan
    logging.info("Successfully connected to the database")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
    raise e

# Koleksi pengguna
ecg_data_collection = db['ecg_data']  # Menggunakan koleksi 'ecg_data'

@app.route('/ecg', methods=['POST'])
def ecg_data():
    try:
        data = request.json
        ecg_value = data.get('value')
        ecg_data_collection.insert_one({"value": ecg_value})  # Menambahkan nilai ECG ke dalam koleksi
        logging.info(f"Received ECG value: {ecg_value}")
        return jsonify({"message": "Data received", "ecg_value": ecg_value}), 200
    except Exception as e:
        logging.error(f"Error in /ecg POST: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ecg', methods=['GET'])
def get_ecg_data():
    try:
        count = request.args.get('count', default=10, type=int)
        ecg_data_cursor = ecg_data_collection.find().sort('_id', -1).limit(count)
        recent_ecg_data = [doc['value'] for doc in ecg_data_cursor]

        # Menghitung rata-rata bergerak
        moving_average = sum(recent_ecg_data) / len(recent_ecg_data) if recent_ecg_data else 0

        return jsonify({
            "message": f"Last {count} ECG data and their moving average",
            "ecg_data": recent_ecg_data,
            "moving_average": moving_average
        }), 200
    except Exception as e:
        logging.error(f"Error in /ecg GET: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ecg/all', methods=['GET'])
def get_all_ecg_dataMv():
    try:
        ecg_data_cursor = ecg_data_collection.find()
        all_ecg_data = [{"dataValue": doc['dataValue']} for doc in ecg_data_cursor]

        return jsonify({
            "message": "All ECG data",
            "ecg_data": all_ecg_data
        }), 200
    except Exception as e:
        logging.error(f"Error in /ecg/all GET: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ecg/init', methods=['POST'])
def init_ecg_data():
    initial_values = [
        0.17494176, 0.7789616, 0.04383012, 0.97437227, 0.0258331, 0.26842418, 0.8858899,
        0.8400674, 0.1127252, 0.7678927, 0.05027479, 0.4220191, 0.28482896, 0.29866636,
        0.34699103, 0.59711796, 0.4650578, 0.54910076, 0.3821269, 0.35992658, 0.09933207,
        0.7916235, 0.7897654, 0.88296384, 0.34732896, 0.1700871, 0.9484916, 0.69737184,
        0.7265282, 0.7889571, 0.6783029, 0.10450809, 0.22405277, 0.19087355, 0.9326232,
        0.5816306, 0.38012153, 0.11534778, 0.3569215, 0.01962687, 0.05663484, 0.15663294,
        0.7757964, 0.4326029, 0.95475245, 0.08347365, 0.04659933, 0.8559404, 0.5395452,
        0.07429481, 0.10580011, 0.9208696, 0.31370166, 0.18684122, 0.9059039, 0.7768382,
        0.8586901, 0.15604386, 0.31430686, 0.6167901, 0.51641595, 0.92676383, 0.16183351,
        0.06466606, 0.5527167, 0.48738942, 0.39009503, 0.8090722, 0.70929825, 0.978139,
        0.9747297, 0.9065552, 0.15241031, 0.48836434, 0.53736085, 0.78921586, 0.7442212,
        0.60346055, 0.5627185, 0.00804049, 0.81561524, 0.71132547, 0.98369914, 0.28949362,
        0.62369734, 0.18071687, 0.95353013, 0.40115196, 0.6317469, 0.33663264, 0.6714114,
        0.98292136, 0.31337124, 0.17296337, 0.8011195, 0.16425253, 0.05180711, 0.65671,
        0.84987134, 0.9425544, 0.5582737, 0.09141523, 0.21328525, 0.39837655, 0.50731146,
        0.33564368, 0.38788337, 0.9851043, 0.86678123, 0.282209, 0.5317597, 0.5674766,
        0.19644164, 0.06424084, 0.2502034, 0.24478297, 0.23281448, 0.01313309, 0.10818172,
        0.52657, 0.07734563, 0.41628385, 0.291383, 0.1691591, 0.5647593, 0.28012252,
        0.63272893, 0.18577872, 0.4182745, 0.92326236, 0.4588622, 0.5772674, 0.84243816,
        0.9675895, 0.87895954, 0.99615955, 0.9504363, 0.8285234, 0.02950887, 0.5199652,
        0.25677893, 0.12071279, 0.49580008, 0.9093509, 0.9786456, 0.43171006, 0.15457746,
        0.2937547, 0.7613733, 0.3474604, 0.9250847, 0.3838063, 0.7214872, 0.15757784,
        0.61181116, 0.88692087, 0.8630734, 0.47760358, 0.8790774, 0.3572927, 0.22043361,
        0.3756388, 0.44135725, 0.09255899, 0.8697755, 0.46885774, 0.50580907, 0.80422664,
        0.76260847, 0.13751167, 0.05669732, 0.51524174, 0.8383471, 0.7548253, 0.25574684,
        0.31011736, 0.49533302, 0.01309227, 0.9259079, 0.52791584, 0.84883755, 0.95005244,
        0.9198237, 0.95364165, 0.9780751, 0.70681435
    ]
    ecg_data_collection.insert_one({"dataValue": initial_values})  # Menambahkan nilai awal sebagai satu dokumen
    logging.info(f"Initial ECG values added: {initial_values}")
    return jsonify({"message": "Initial data added", "initial_values": initial_values}), 200


@app.route('/ecg/add', methods=['POST'])
def add_ecg_data():
    try:
        data = request.json
        ecg_values = data.get('dataValue')
        ecg_data_collection.insert_one({"dataValue": ecg_values})  # <- Menambahkan nilai baru sebagai satu dokumen
        logging.info(f"New ECG values added: {ecg_values}")
        return jsonify({"message": "Data added", "dataValue": ecg_values}), 200
    except Exception as e:
        logging.error(f"Error in /ecg/add POST: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/ecg/get_latestEcg', methods=['GET'])
def get_latest_ecg_data():
    try:
        # Mengambil dokumen terbaru
        latest_ecg_data = ecg_data_collection.find_one(
            sort=[('_id', -1)]
        )
        
        if latest_ecg_data:
            logging.info(f"Retrieved latest ECG data: {latest_ecg_data['dataValue']}")
            return jsonify({"message": "Latest ECG data retrieved", "dataValue": latest_ecg_data['dataValue']}), 200
        else:
            return jsonify({"message": "No ECG data found"}), 404
    except Exception as e:
        logging.error(f"Error in /ecg/get_latest GET: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/ecg/get_allData', methods=['GET'])
def get_all_ecg_data():
    try:
        # Mengambil semua dokumen dari koleksi
        ecg_data_cursor = ecg_data_collection.find()
        all_ecg_data = [{"dataValue": doc['dataValue']} for doc in ecg_data_cursor]
        
        if all_ecg_data:
            logging.info(f"Retrieved all ECG data.")
            return jsonify({"message": "All ECG data retrieved", "data": all_ecg_data}), 200
        else:
            return jsonify({"message": "No ECG data found"}), 404
    except Exception as e:
        logging.error(f"Error in /ecg/get_all GET: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
