from flask import Flask, jsonify, request

app2 = Flask(__name__)
as_ip = None
as_port = None
fs_hostname = None
fs_ip = None

@app2.route("/fibonacci", methods=['GET'])

def get_sequence():
    number = request.args.get('number', type=int)

    if number is None:
        return jsonify({'error': 'number parameter must be an int'}), 400

    #n = int(number)

    return jsonify({'number': number})

@app2.route('/register', methods=['PUT'])
def get_details():
    global fs_hostname, fs_ip, as_ip, as_port

    if request.is_json:
        registration_data = request.get_json()

        fs_hostname = registration_data.get('hostname')
        fs_ip = registration_data.get('ip')
        as_ip = registration_data.get('as_ip')
        as_port = registration_data.get('as_port')

        if fs_hostname and fs_ip and as_ip and as_port:
            return jsonify({"message": "Registration data recieved"}), 200
        else:
            return jsonify({'error':"Error in data"}), 400
    else:
        return jsonify({'error': "Data must be in json format"}), 400

if __name__ == "__main__":
    app2.run(host="0.0.0.0", port=9090, debug=True)