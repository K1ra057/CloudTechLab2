from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = "cars.json"

# Загрузка из файла
def load_cars():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Сохранение в файл
def save_cars():
    with open(DATA_FILE, "w") as f:
        json.dump(cars, f, indent=2)

cars = load_cars()

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

@app.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(cars)

@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    car = next((c for c in cars if c["id"] == car_id), None)
    return jsonify(car) if car else (jsonify({"error": "Car not found"}), 404)

@app.route("/cars", methods=["POST"])
def add_car():
    data = request.json
    new_car = {
        "id": max([c["id"] for c in cars], default=0) + 1,
        "brand": data.get("brand"),
        "model": data.get("model"),
        "year": data.get("year"),
    }
    cars.append(new_car)
    save_cars()
    return jsonify(new_car), 201

@app.route("/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    data = request.json
    car = next((c for c in cars if c["id"] == car_id), None)
    if car:
        car.update(data)
        save_cars()
        return jsonify(car)
    return jsonify({"error": "Car not found"}), 404

@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    global cars
    cars = [c for c in cars if c["id"] != car_id]
    save_cars()
    return jsonify({"message": "Car deleted"})

if __name__ == "__main__":
    app.run(debug=True)
