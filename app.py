# app.py
from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Cargar el modelo entrenado
model = joblib.load("modelo_entrenado.pkl")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET","POST"])
def predict():
    data = request.form.to_dict()
    print("Data received:", data) 
    bedrooms = float(data.get("bedrooms", 0))
    bathrooms = float(data.get("bathrooms", 0))
    area = float(data.get("area", 0))
    year = float(data.get("year", 0))
    metro = data.get("metro", False)
    renfe = data.get("renfe", False)
    air_conditioning = data.get("air_conditioning", False)
    elevator = data.get("elevator", False)
    garden = data.get("garden", False)
    property_type = data.get("property_type", "")
    etiqueta = data.get("label", "")
    district = data.get("district", "")
    print("hola que t")
    print(1)
    # Preprocesar los datos (si es necesario)
    # Hacer la predicción
    #prediction = model.predict([[bedrooms, bathrooms, area]])
    
    #return jsonify({"prediction": prediction[0]})
    return jsonify({"prediction": 115})


if __name__ == "__main__":
    app.run(debug=True)

