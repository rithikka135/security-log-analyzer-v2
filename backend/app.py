from flask import Flask, request, jsonify
from flask_cors import CORS
from logs_db import add_log, get_logs

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Security Log Analyzer API Running!"

# GET route for testing /add/<msg>
@app.route("/add/<msg>")
def add(msg):
    add_log(msg)
    return f"Added log: {msg}"

# ✅ New POST route to accept JSON
@app.route("/log", methods=["POST"])
def add_log_json():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message'"}), 400
    msg = data["message"]
    add_log(msg)
    return jsonify({"message": msg, "status": "success"})

# GET route to fetch all logs
@app.route("/logs")
def logs():
    return jsonify({"logs": get_logs()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)