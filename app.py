# app.py
from flask import Flask, render_template, request, jsonify
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import PolynomialFeatures, StandardScaler,OneHotEncoder
import pandas as pd


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
    house_type = data.get("housing_type", "")
    etiqueta = data.get("label", "")
    district = data.get("district", "")
    diccionario = {
        "Dormitorios":bedrooms,
        "Superficie":area,
        "Num_baños":bathrooms,
        "Metro":metro,
        "Renfe":renfe,
        "Tipo_de_inmueble":property_type,
        "Año_de_construccion":year,
        "Calefaccion":air_conditioning,
        "Etiqueta":etiqueta,
        "Aire acondicionado":air_conditioning,
        "Ascensor":elevator,
        "Jardin":garden,
        "Tipo":house_type,
        "distrito/ciudad":district,
    }
    print(1)
    CordenasPorDistritos = pd.read_csv("static/CordenadasPorDistrito.csv")
    diccionario["Latitud"] = CordenasPorDistritos[CordenasPorDistritos["distrito/ciudad"]=="Alameda de Osuna"]["Latitud"].values
    diccionario["Longitud"] = CordenasPorDistritos[CordenasPorDistritos["distrito/ciudad"]=="Alameda de Osuna"]["Longitud"].values
    inputPrediccion = pd.DataFrame(diccionario)
    # Preprocesar los datos (si es necesario)
    # Hacer la predicción
    prediction = model.predict(inputPrediccion)
    
    return jsonify({"prediction": prediction[0]})
    #return jsonify({"prediction": 115})


if __name__ == "__main__":
    app.run(debug=True)

