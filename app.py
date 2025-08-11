# app.py
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from utils.parser import extract_text
from model import load_model, ensure_dirs
import joblib
import json
from datetime import datetime

UPLOAD_FOLDER = "uploads"
ALLOWED_EXT = {"pdf","docx","txt"}

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB

ensure_dirs()
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
model = load_model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # expects: 'resume' file and 'job' text (job description)
    job_desc = request.form.get("job", "").strip()
    file = request.files.get("resume")
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        text = extract_text(file)
    else:
        return jsonify({"error": "upload a .pdf/.docx/.txt file"}), 400

    # Prepare input text: combine resume + job for scoring strategy: here we'll score resume vs job by concatenation approach
    # Approach: compute probability that resume contains job-keywords by passing job description as "positive" training proxy.
    # Simpler: compute probability of job_desc + resume being positive using existing model: we will score both: resume alone & combined.
    if not job_desc:
        job_desc = "data analysis python sql machine learning nlp power bi oci"

    # Predict using the pipeline
    pipeline = model
    try:
        score_resume = pipeline.predict_proba([text])[0][1]
        # Also derive a simple keyword overlap percentage for explanation
        job_tokens = set(job_desc.lower().split())
        resume_tokens = set(text.lower().split())
        common = job_tokens.intersection(resume_tokens)
        overlap_pct = round(100.0 * len(common) / max(1, len(job_tokens)), 1)
        # top matched keywords (intersection limited)
        matched = list(common)[:12]
        result = {
            "score": round(float(score_resume), 4),
            "match_percent_keywords": overlap_pct,
            "matched_keywords": matched,
            "text_snippet": text[:1000].replace("\n"," ") + ("..." if len(text)>1000 else "")
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error":"prediction failed","detail":str(e)}), 500

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
