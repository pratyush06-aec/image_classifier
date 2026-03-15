from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy 
import os, sqlite3
from model import classify_image

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///classifier.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
# db= SQLAlchemy(app)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    prediction = classify_image(filepath)

    conn = sqlite3.connect("classifier.db")
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