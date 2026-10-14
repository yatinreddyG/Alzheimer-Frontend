"""
Alzheimer's Disease Detection - FRONT-END ONLY build (Review-2 prototype).

Scope: all web pages + MRI image upload (validation, secure save, preview).
NOT included yet: preprocessing, CNN model, prediction, Grad-CAM, PDF report.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import os
import time
import uuid

from flask import (
    Flask, render_template, request, redirect, url_for, flash,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def unique_secure_filename(original):
    """Collision-free, path-traversal-safe filename."""
    safe = secure_filename(original) or "upload"
    name, ext = os.path.splitext(safe)
    return f"{name}_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"


def has_valid_image_signature(stream):
    """Check magic bytes so a renamed non-image file is rejected."""
    head = stream.read(8)
    stream.seek(0)
    return head.startswith(b"\xff\xd8\xff") or head.startswith(b"\x89PNG\r\n\x1a\n")


@app.context_processor
def inject_asset_versioning():
    """Cache-busting helper: {{ asset_url('css/style.css') }}"""
    def asset_url(relative_path):
        full = os.path.join(app.static_folder, relative_path)
        try:
            version = int(os.path.getmtime(full))
        except OSError:
            version = 0
        return f"{url_for('static', filename=relative_path)}?v={version}"
    return dict(asset_url=asset_url)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict_route():
    if request.method == "GET":
        return render_template("predict.html")

    if "mri_image" not in request.files:
        flash("No file part in the request.", "danger")
        return redirect(url_for("predict_route"))

    file = request.files["mri_image"]
    if file.filename == "":
        flash("Please choose an MRI image before submitting.", "danger")
        return redirect(url_for("predict_route"))

    if not is_allowed_file(file.filename):
        flash("Unsupported file type. Please upload a JPG, JPEG, or PNG image.",
              "danger")
        return redirect(url_for("predict_route"))

    # Validate magic bytes BEFORE saving, so fake images never touch disk.
    if not has_valid_image_signature(file.stream):
        flash("The file is not a valid JPG/PNG image.", "danger")
        return redirect(url_for("predict_route"))

    filename = unique_secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    info = {
        "filename": filename,
        "original_name": file.filename,
        "size_kb": round(os.path.getsize(save_path) / 1024, 1),
        "file_type": os.path.splitext(filename)[1].lstrip(".").upper(),
    }
    return render_template("upload_success.html", info=info)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(_exc):
    flash("The uploaded file is too large. Maximum allowed size is 10 MB.", "danger")
    return redirect(url_for("predict_route"))


@app.errorhandler(404)
def handle_404(_exc):
    return render_template("404.html"), 404


@app.errorhandler(500)
def handle_500(_exc):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=True)
