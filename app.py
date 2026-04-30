from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy 
import os, sqlite3
from model import classify_image
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///classifier.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
# db= SQLAlchemy(app)

DB_PATH= "instance/classifier.db"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    if file.filename == "":
        return "No file selected"
    filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    prediction = classify_image(filepath)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO predictions (image_path, prediction) VALUES (?, ?)",
        (filepath, prediction)
    )

    conn.commit()
    conn.close()

    return render_template("result.html", prediction=prediction, image=filepath)

if __name__ == "__main__":
    app.run(debug=True, port=8000)



# We can change the port of our local-host by adding our customized port in our code itself