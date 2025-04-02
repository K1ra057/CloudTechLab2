from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# Тимчасове сховище даних (список машин)
cars = [
    {"id": 1, "brand": "Toyota", "model": "Corolla", "year": 2020},
    {"id": 2, "brand": "Honda", "model": "Civic", "year": 2019},
]

# Головна сторінка (віддає HTML-файл)
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

# Отримати список всіх машин
@app.route("/cars", methods=["GET"])
def get_cars():
    return jsonify(cars)

# Отримати конкретну машину за ID
@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    car = next((c for c in cars if c["id"] == car_id), None)
    return jsonify(car) if car else (jsonify({"error": "Car not found"}), 404)

# Додати нову машину
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
    return jsonify(new_car), 201

# Оновити дані машини
@app.route("/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    data = request.json
    car = next((c for c in cars if c["id"] == car_id), None)
    if car:
        car.update(data)
        return jsonify(car)
    return jsonify({"error": "Car not found"}), 404

# Видалити машину
@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    global cars
    cars = [c for c in cars if c["id"] != car_id]
    return jsonify({"message": "Car deleted"})

if __name__ == "__main__":
    app.run(debug=True)
