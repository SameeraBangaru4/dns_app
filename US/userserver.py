from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

@app.route("/fibonacci", methods=['GET'])
def get_params():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return jsonify({"error": "Missing query parameters"}), 400
    
    try:
        fs_port = int(fs_port)
        as_port = int(as_port)
        number = int(number)
    except ValueError:
        return jsonify({'error': 'Ports and number must be intergers'})
    
    as_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = f"NAME={hostname}\nTYPE=A\n"

    try:
        as_sock.sendto(message.encode(), (as_ip, as_port))
        as_sock.settimeout(20)
        data, _ = as_sock.recvfrom(1024)
        response = data.decode().splitlines()

        fs_ip = None
        for line in response:
            if line.startswith("VALUE="):
                fs_ip = line.split("=", 1)[1].strip()
        if not fs_ip:
            return jsonify({'error': 'AS did not return IP'}), 500
    except Exception as e:
        return jsonify({'error': f'Error contacting AS:{e}'}), 500
    finally:
        as_sock.close()

    fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    
    try:
        r = requests.get(fs_url)
        if r.status_code != 200:
            return jsonify({'error': f'Error at the FS returned {r.status_code}'}), 500
        return jsonify(r.json()), 200
    except Exception as e:
        return jsonify({'error': f"Error contacting FS: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
