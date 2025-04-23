from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Подключение к базе данных MySQL (указываем URI для подключения через SQLAlchemy)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:prhFZETaRWzNFGMcYAyClmmhdinUsKYv@gondola.proxy.rlwy.net:17227/Xmara"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Определяем модель для таблицы cars
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Car {self.brand} {self.model}>"

# Создание таблиц, если их нет
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

@app.route("/cars", methods=["GET"])
def get_cars():
    cars = Car.query.all()  # Получаем все записи из таблицы
    return jsonify([{"id": car.id, "brand": car.brand, "model": car.model, "year": car.year} for car in cars])

@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    car = Car.query.get(car_id)  # Получаем одну машину по ID
    if car:
        return jsonify({"id": car.id, "brand": car.brand, "model": car.model, "year": car.year})
    return jsonify({"error": "Car not found"}), 404

@app.route("/cars", methods=["POST"])
def add_car():
    data = request.json
    new_car = Car(
        brand=data.get("brand"),
        model=data.get("model"),
        year=data.get("year")
    )
    db.session.add(new_car)
    db.session.commit()  # Сохраняем новый объект в БД
    return jsonify({"id": new_car.id, "brand": new_car.brand, "model": new_car.model, "year": new_car.year}), 201

@app.route("/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    data = request.json
    car = Car.query.get(car_id)
    if car:
        car.brand = data.get("brand")
        car.model = data.get("model")
        car.year = data.get("year")
        db.session.commit()
        return jsonify({"id": car.id, "brand": car.brand, "model": car.model, "year": car.year})
    return jsonify({"error": "Car not found"}), 404

@app.route("/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
        return jsonify({"message": "Car deleted"})
    return jsonify({"error": "Car not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
