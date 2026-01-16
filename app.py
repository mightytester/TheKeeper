import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Path configuration
TO_REVIEW = os.environ.get("REVIEW_PATH", "images/to_review")
SELECTED = os.path.join(TO_REVIEW, "selected")
DISCARDED = os.path.join(TO_REVIEW, "discarded")

for d in [TO_REVIEW, SELECTED, DISCARDED]:
    os.makedirs(d, exist_ok=True)

def get_images():
    return sorted([
        f for f in os.listdir(TO_REVIEW)
        if os.path.isfile(os.path.join(TO_REVIEW, f)) and
           f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ])

@app.route("/")
def index():
    images = get_images()
    return render_template("index.html", images=images)

@app.route("/process", methods=["POST"])
def process():
    selected = request.form.getlist("selected")
    action = request.form.get("action")
    all_images = set(get_images())

    if action == "keep_selected_discard_rest":
        # Keep selected, discard all others
        for img in selected:
            shutil.move(os.path.join(TO_REVIEW, img), os.path.join(SELECTED, img))
        for img in all_images - set(selected):
            shutil.move(os.path.join(TO_REVIEW, img), os.path.join(DISCARDED, img))
    elif action == "keep_selected_only":
        # Keep only selected, leave others in place
        for img in selected:
            shutil.move(os.path.join(TO_REVIEW, img), os.path.join(SELECTED, img))
    elif action == "discard_selected_only":
        # Discard only selected, leave others in place
        for img in selected:
            shutil.move(os.path.join(TO_REVIEW, img), os.path.join(DISCARDED, img))

    return redirect(url_for("index"))

@app.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(TO_REVIEW, filename)

if __name__ == "__main__":
    path = os.environ.get("REVIEW_PATH", TO_REVIEW)
    print(f"Reviewing images from: {os.path.abspath(path)}")
    app.run(host="0.0.0.0", port=5000, debug=True)

