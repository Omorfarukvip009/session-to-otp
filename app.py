from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = "sessions"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_ID = 21599456
API_HASH = "92adb31104272bb579d57fbfe88b960d"
current_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    global current_process

    # Stop previous process if running
    if current_process and current_process.poll() is None:
        current_process.terminate()

    if "session_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["session_file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    session_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(session_path)

    # Run login.py as subprocess
    current_process = subprocess.Popen(
        ["python", "login.py", str(API_ID), API_HASH, session_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    return jsonify({"message": "Session uploaded and login started!"})

@app.route("/logs")
def logs():
    global current_process
    if current_process:
        output = current_process.stdout.read()
        return jsonify({"logs": output})
    return jsonify({"logs": ""})

@app.route("/next", methods=["POST"])
def next_session():
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
    return jsonify({"message": "Ready for next session!"})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
  
