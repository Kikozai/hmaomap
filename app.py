from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///landmarks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель базы данных
class Landmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

@app.route("/")
def map_view():
    landmarks = Landmark.query.all()
    landmarks_data = [
        {
            "name": lm.name,
            "address": lm.address,
            "latitude": lm.latitude,
            "longitude": lm.longitude
        }
        for lm in landmarks
    ]
    return render_template("map.html", landmarks=landmarks_data)

if __name__ == "__main__":
    app.run(debug=True)
