from flask import Flask, jsonify, request
import socket
app2 = Flask(__name__)
as_ip = None
as_port = None
fs_hostname = None
fs_ip = None
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1

    for _ in range(2, n+1):
        a, b = b, a+b

    return b
@app2.route("/fibonacci", methods=['GET'])

def get_sequence():
    number = request.args.get('number')

    if number is None:
        return jsonify({'error': 'number parameter is required'}), 400
    
    try:
        n = int(number)
    except ValueError:
        return jsonify({'error': 'number must be an interger'}), 400
    
    if n < 0:
        return jsonify({'error': 'Number must be positive'}), 400
    fib_value = fibonacci(n)

    return jsonify({'number': fib_value}), 200

@app2.route('/register', methods=['PUT'])
def get_details():
    global fs_hostname, fs_ip, as_ip, as_port

    if request.is_json:
        registration_data = request.get_json()

        fs_hostname = registration_data.get('hostname')
        fs_ip = registration_data.get('ip')
        as_ip = registration_data.get('as_ip')
        as_port = int(registration_data.get('as_port'))

        if not fs_hostname or not fs_ip or not as_ip or not as_port:
            return jsonify({'error':"Error in data"}), 400
    
        registration_with_as(fs_hostname, fs_ip, as_ip, as_port)
        return "Registered", 201
    else:
        return jsonify({'error': "Data must be in json format"}), 400

def registration_with_as(hostname, ip, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:

        sock.sendto(message.encode(), (as_ip, as_port))
    finally:
        sock.close()

if __name__ == "__main__":
    app2.run(host="0.0.0.0", port=9090, debug=True)