# app.py
from flask import Flask, render_template, request, jsonify
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import PolynomialFeatures, StandardScaler,OneHotEncoder
import pandas as pd


import joblib

app = Flask(__name__)

# Cargar el modelo entrenado
model = joblib.load("pkl/modelo_produccion.pkl")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET","POST"])
def predict():
    data = request.form.to_dict()
    print("Data received:", data) 
    area = float(data.get("area", 0))
    bedrooms = float(data.get("bedrooms", 0))
    bathrooms = float(data.get("bathrooms", 0))
    year = float(data.get("year", 0))
    metro = data.get("metro", False)
    renfe = data.get("renfe", False)
    heating = data.get("heating", False)
    air_conditioning = data.get("air_conditioning", False)
    elevator = data.get("elevator", False)
    garden = data.get("garden", False)
    property_type = data.get("property_type", "")
    house_type = data.get("housing_type", "")
    etiqueta = data.get("label", "")
    district = data.get("district", "").strip()

    # Realizar las validaciones
    errors = []

    if area > 300:
        errors.append("La superficie no puede ser mayor a 300 m².")

    if area < 0:
        errors.append("La superficie no puede ser negativa.")

    if bedrooms > 5:
        errors.append("El número de dormitorios no puede ser mayor a 5.")

    if bedrooms < 0:
        errors.append("El número de dormitorios no puede ser negativo.")

    if bathrooms > 4:
        errors.append("El número de baños no puede ser mayor a 4.")

    if bathrooms < 0:
        errors.append("El número de baños no puede ser negativo.")

    if year < 1800 or year > 2024:
        errors.append("El año de construcción debe estar entre 1800 y 2024.")

    # Si hay errores, retornar un mensaje de error
    if errors:
        return jsonify({"error": errors})

    diccionario = {
        "Dormitorios":bedrooms,
        "Superficie":area,
        "Num_baños":bathrooms,
        "Metro":metro,
        "Renfe":renfe,
        "Tipo_de_inmueble":property_type,
        "Año_de_construccion":year,
        "Calefaccion":heating,
        "Etiqueta":etiqueta,
        "Aire acondicionado":air_conditioning,
        "Ascensor":elevator,
        "Jardin":garden,
        "Tipo":house_type,
        "distrito/ciudad":district,
    }
    CordenadasPorDistritos = pd.read_csv("static/CordenadasPorDistrito.csv")
    diccionario["Latitud"] = CordenadasPorDistritos[CordenadasPorDistritos["distrito/ciudad"]==district]["Latitud"].values
    diccionario["Longitud"] = CordenadasPorDistritos[CordenadasPorDistritos["distrito/ciudad"]==district]["Longitud"].values
    inputPrediccion = pd.DataFrame(diccionario)
    numeric_columns = ['Dormitorios', 'Superficie', 'Num_baños', 'Metro', 'Renfe', 'Año_de_construccion', 'Calefaccion',
                   'Aire acondicionado', 'Ascensor', 'Jardin']
    # Convertir las columnas a enteros
    for column in numeric_columns:
        inputPrediccion[column] = pd.to_numeric(inputPrediccion[column], errors='coerce').astype(int)
    encoder = joblib.load('pkl/encoderProduccion.pkl')
    inputPrediccionEncoded = one_hot_encoding_row(inputPrediccion,encoder)
    inputPrediccionEncodedScalaed = estandarizar(inputPrediccionEncoded)
    # Preprocesar los datos (si es necesario)
    # Hacer la predicción
    prediction = model.predict(inputPrediccionEncodedScalaed)
    return jsonify({"prediction": prediction[0]})


##Funciones auxiliares
def one_hot_encoding_row(dato_row, encoder):
    # Obtenemos las columnas categóricas
    categorical_columns = dato_row.select_dtypes(include=["object"]).columns
    
    # Aplicamos la codificación one-hot usando el encoder previamente ajustado
    encoded_columns = encoder.transform(dato_row[categorical_columns])
    new_columns = encoder.get_feature_names_out(categorical_columns)
    
    # Creamos un DataFrame con las columnas codificadas
    data_encoded = pd.DataFrame(encoded_columns, columns=new_columns)
    
    # Concatenamos las columnas codificadas con el resto de la fila de datos
    dato_row_encoded = pd.concat([dato_row.drop(categorical_columns, axis=1), data_encoded], axis=1)
    
    return dato_row_encoded

def estandarizar(dato_encoded):
    scaler = joblib.load('pkl/scalerProduccion.pkl')
    variables_estandarizar = ["Dormitorios","Superficie","Num_baños","Año_de_construccion","Latitud","Longitud"]
    dato_encoded[variables_estandarizar] = scaler.transform(dato_encoded[variables_estandarizar])
    return dato_encoded

    

if __name__ == "__main__":
    app.run(debug=True,port=8000)

