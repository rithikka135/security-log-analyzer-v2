from flask import Flask, request, jsonify
from flask_cors import CORS
from logs_db import add_log, get_logs

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Security Log Analyzer API Running!"

# POST route to accept JSON with username, ip, status, and optional message
@app.route("/log", methods=["POST"])
def add_log_json():
    data = request.get_json()
    if not data or "username" not in data or "ip" not in data or "status" not in data:
        return jsonify({"error": "Missing one of the required fields: username, ip, status"}), 400

    username = data["username"]
    ip = data["ip"]
    status = data["status"]
    message = data.get("message")  # optional

    add_log(username, ip, status, message)

    return jsonify({
        "message": f"{username} {status} from {ip}",
        "status": "success"
    })

# GET route to fetch all logs
@app.route("/logs")
def logs():
    logs_list = get_logs()
    return jsonify({"logs": logs_list})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)