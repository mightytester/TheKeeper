import os
import shutil
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TO_REVIEW = os.path.join(BASE_DIR, "images/to_review")
SELECTED = os.path.join(BASE_DIR, "images/selected")
DISCARDED = os.path.join(BASE_DIR, "images/discarded")

for d in [TO_REVIEW, SELECTED, DISCARDED]:
    os.makedirs(d, exist_ok=True)

def get_images():
    return sorted([
        f for f in os.listdir(TO_REVIEW)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ])

@app.route("/")
def index():
    images = get_images()
    return render_template("index.html", images=images)

@app.route("/process", methods=["POST"])
def process():
    selected = request.form.getlist("selected")
    all_images = set(get_images())

    # Move kept images
    for img in selected:
        shutil.move(
            os.path.join(TO_REVIEW, img),
            os.path.join(SELECTED, img)
        )

    # Move remaining to discarded
    for img in all_images - set(selected):
        shutil.move(
            os.path.join(TO_REVIEW, img),
            os.path.join(DISCARDED, img)
        )

    return redirect(url_for("index"))

@app.route("/images/<filename>")
def serve_image(filename):
    return app.send_from_directory(TO_REVIEW, filename)

if __name__ == "__main__":
    app.run(debug=True)
