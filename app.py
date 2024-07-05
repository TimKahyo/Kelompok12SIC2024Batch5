from flask import Flask, request, jsonify

app = Flask(__name__)

ecg_data_list = []  # List untuk menyimpan data ECG

@app.route('/ecg', methods=['POST'])
def ecg_data():
    data = request.json
    ecg_value = data.get('value')
    ecg_data_list.append(ecg_value)  # Menambahkan nilai ECG ke dalam list
    # Melakukan sesuatu dengan data ECG (misalnya, menyimpan ke database)
    print(f"Received ECG value: {ecg_value}")
    return jsonify({"message": "Data received", "ecg_value": ecg_value}), 200

@app.route('/ecg', methods=['GET'])
def get_ecg_data():
    # Mengambil jumlah data yang diinginkan dari parameter query 'count'
    count = request.args.get('count', default=10, type=int)
    
    # Mengambil data terakhir sesuai dengan jumlah 'count'
    recent_ecg_data = ecg_data_list[-count:]

    # Menghitung rata-rata bergerak
    moving_average = sum(recent_ecg_data) / len(recent_ecg_data) if recent_ecg_data else 0

    return jsonify({
        "message": f"Last {count} ECG data and their moving average",
        "ecg_data": recent_ecg_data,
        "moving_average": moving_average
    }), 200

@app.route('/ecg/all', methods=['GET'])
def get_all_ecg_data():
    # Menghitung rata-rata bergerak dari semua data ECG yang ada
    moving_average = sum(ecg_data_list) / len(ecg_data_list) if ecg_data_list else 0

    return jsonify({
        "message": "All ECG data and their moving average",
        "ecg_data": ecg_data_list,
        "moving_average": moving_average
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




# RUN : 
# 1. env\Scripts\activate
# 2. python app.py