from flask import Flask, render_template, request, jsonify
import subprocess, os

app = Flask(__name__)
UPLOAD_FOLDER = "sessions"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_ID = 21599456
API_HASH = "92adb31104272bb579d57fbfe88b960d"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_run", methods=["POST"])
def upload_run():
    if "session_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["session_file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    session_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(session_path)

    try:
        # Run login.py and capture full output
        result = subprocess.run(
            ["python", "login.py", str(API_ID), API_HASH, session_path],
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)

    return jsonify({"output": output})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    
