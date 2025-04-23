from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Подключение к Railway MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:prhFZETaRWzNFGMcYAyClmmhdinUsKYv@gondola.proxy.rlwy.net:17227/Xmara"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Модель машины
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Создание таблицы, если её нет
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

@app.route("/cars", methods=["GET"])
def get_cars():
    cars = Car.query.all()
    return jsonify([{
        "id": c.id,
        "brand": c.brand,
        "model": c.model,
        "year": c.year
    } for c in cars])

@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    car = Car.query.get(car_id)
    return jsonify({
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year
    }) if car else (jsonify({"error": "Car not found"}), 404)

@app.route("/cars", methods=["POST"])
def add_car():
    data = request.json
    car = Car(brand=data["brand"], model=data["model"], year=data["year"])
    db.session.add(car)
    db.session.commit()
    return jsonify({
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year
    }), 201

@app.route("/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    data = request.json
    car.brand = data.get("brand", car.brand)
    car.model = data.get("model", car.model)
    car.year = data.get("year", car.year)
    db.session.commit()
    return jsonify({
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year
    })

@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted"})

if __name__ == "__main__":
    app.run(debug=True)
