from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from logs_db import add_log, get_logs
import os

app = Flask(__name__)
CORS(app)

# Get frontend path correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Home route
@app.route("/")
def home():
    return "Security Log Analyzer API Running!"

# Add log
@app.route("/log", methods=["POST"])
def add_log_json():
    data = request.get_json()

    if not data or "username" not in data or "ip" not in data or "status" not in data:
        return jsonify({"error": "Missing fields"}), 400

    username = data["username"]
    ip = data["ip"]
    status = data["status"]
    message = data.get("message", "")

    add_log(username, ip, status, message)

    return jsonify({
        "message": f"{username} {status} from {ip}",
        "status": "success"
    })

# Get logs
@app.route("/logs")
def logs():
    logs_list = get_logs()

    formatted_logs = []
    for log in logs_list:
        formatted_logs.append({
            "id": log[0],
            "username": log[1],
            "ip": log[2],
            "status": log[3],
            "message": log[4],
            "timestamp": log[5]
        })

    return jsonify({"logs": formatted_logs})

# Analyze logs
@app.route("/analyze")
def analyze():
    logs_list = get_logs()

    failed = []
    success = 0

    for log in logs_list:
        if log[3].lower() == "failed":
            failed.append(log)
        else:
            success += 1

    return jsonify({
        "total_logs": len(logs_list),
        "failed_attempts": len(failed),
        "successful_attempts": success,
        "suspicious_logs": failed[:10]
    })

# Serve frontend (MAIN FIX)
@app.route("/ui")
def serve_ui():
    return send_from_directory(FRONTEND_DIR, "index.html")

# Serve static files (CSS, JS)
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory(os.path.join(FRONTEND_DIR, "static"), path)

# Run app (Railway compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)