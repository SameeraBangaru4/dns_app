from flask import Flask, request, jsonify

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
    
    
    return jsonify({
        "hostname": hostname,
        "fs_port": fs_port,
        "number": number,
        "as_ip": as_ip,
        "as_port": as_port
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
