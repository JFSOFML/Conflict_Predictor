import sqlite3
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# Initialize the FastAPI application
app = FastAPI()

# Load the models from the pickle files
with open("models/Scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("models/forest.pkl", "rb") as f:
    forest = pickle.load(f)
with open("models/SVCModel_pipeline.pkl", "rb") as f:
    SVCModel_pipeline = pickle.load(f)


class TitanicInput(BaseModel):
    """Pydantic model for Titanic input data"""
    Pclass: int
    Sex: int
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: int


class HousingInput(BaseModel):
    """Pydantic model for Housing input data"""
    # Define the required fields for the housing model
    feature_1: float
    feature_2: float
    # Add other features based on your dataset


def execute_query(query: str):
    """
    Function to execute SQL queries.

    :param query: SQL query to execute
    :return: Dictionary with columns and data or error message
    """
    try:
        conn = sqlite3.connect("/app/DSRA_projects.db")
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        data = cursor.fetchall()
        conn.close()
        return {"columns": columns, "data": data}
    except sqlite3.Error as e:
        return {"error": str(e)}


@app.post("/predict_titanic")
def predict_titanic(data: TitanicInput):
    """
    Predict survival on Titanic based on the input data.

    :param data: TitanicInput object containing features
    :return: Dictionary with prediction result
    """
    df = pd.DataFrame([data.dict()])
    prediction = SVCModel_pipeline.predict(df)[0]
    return {"Survived": int(prediction)}


@app.post("/predict_housing")
def predict_housing(data: HousingInput):
    """
    Predict housing prices based on the input data.

    :param data: HousingInput object containing features
    :return: Dictionary with price prediction result
    """
    df = pd.DataFrame([data.dict()])
    scaled_data = scaler.transform(df)
    prediction = forest.predict(scaled_data)[0]
    return {"price": float(prediction)}


@app.post("/query")
def query(query: str):
    """
    Execute an SQL query on the database.

    :param query: SQL query string
    :return: Query results or error message
    """
    result = execute_query(query)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
