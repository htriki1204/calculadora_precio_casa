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
    diccionario["Latitud"] = CordenasPorDistritos[CordenasPorDistritos["distrito/ciudad"]==district]["Latitud"].values
    diccionario["Longitud"] = CordenasPorDistritos[CordenasPorDistritos["distrito/ciudad"]==district]["Longitud"].values
    inputPrediccion = pd.DataFrame(diccionario)
    numeric_columns = ['Dormitorios', 'Superficie', 'Num_baños', 'Metro', 'Renfe', 'Año_de_construccion', 'Calefaccion',
                   'Aire acondicionado', 'Ascensor', 'Jardin']
    # Convertir las columnas a enteros
    for column in numeric_columns:
        inputPrediccion[column] = pd.to_numeric(inputPrediccion[column], errors='coerce').astype(int)
    encoder = joblib.load('encoder.pkl')
    inputPrediccionEncoded = one_hot_encoding_row(inputPrediccion,encoder)
    inputPrediccionEncodedScalaed = estandarizar(inputPrediccionEncoded)
    # Preprocesar los datos (si es necesario)
    # Hacer la predicción
    prediction = model.predict(inputPrediccionEncodedScalaed)
    
    return jsonify({"prediction": prediction[0]})
    #return jsonify({"prediction": 115})


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
    scaler = joblib.load('scaler.pkl')
    variables_estandarizar = ["Dormitorios","Superficie","Num_baños","Año_de_construccion","Latitud","Longitud"]
    dato_encoded[variables_estandarizar] = scaler.transform(dato_encoded[variables_estandarizar])
    return dato_encoded

    

if __name__ == "__main__":
    app.run(debug=True,port=8000)

