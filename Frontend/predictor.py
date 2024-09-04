"""
This module provides the Streamlit frontend for the Maritime and Air Traffic Predictor application.
It interacts with the FastAPI backend to display real-time maritime and air traffic data and allows
users to input traffic data for prediction of slowdowns between Taiwan and China.
"""

import streamlit as st
import requests

# FastAPI Backend URL
API_URL = "http://localhost:8000"
TIMEOUT_DURATION = 10  # Timeout in seconds for all requests

st.title("Maritime and Air Traffic Predictor")

# Function to get prediction from FastAPI
def get_prediction(data: dict):
    """
    Sends prediction request to the FastAPI backend with given input data.

    :param data: Dictionary containing input data for prediction
    :return: JSON response from the FastAPI backend
    """
    try:
        response = requests.post(f"{API_URL}/predict_traffic_slowdown", json=data, timeout=TIMEOUT_DURATION)
        response.raise_for_status()  # Raises HTTPError if the response code was unsuccessful
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to get a response from the API: {e}")

# Sidebar for inputs
st.sidebar.header("Input Data")
# Placeholder for user inputs (customize based on your model's input features)
maritime_traffic = st.sidebar.slider("Maritime Traffic (value)", 0, 100, 50)
air_traffic = st.sidebar.slider("Air Traffic (value)", 0, 100, 50)
historical_data = st.sidebar.checkbox("Use Historical Data")

# Button to trigger prediction
if st.sidebar.button("Predict Slowdown"):
    # Construct the input data for prediction
    input_data = {
        "maritime_traffic": maritime_traffic,
        "air_traffic": air_traffic,
        "historical_data": historical_data,
    }

    # Call the FastAPI backend to get a prediction
    result = get_prediction(input_data)

    # Display the prediction result
    if result:
        st.subheader("Prediction Result")
        st.write(result)

# Display real-time data from maritime and air traffic
st.subheader("Real-Time Traffic Data")

# Fetch maritime traffic data from FastAPI
def fetch_maritime_data():
    """
    Fetches real-time maritime traffic data from the FastAPI backend.

    :return: JSON response with maritime traffic data
    """
    try:
        response = requests.get(f"{API_URL}/maritime_traffic", timeout=TIMEOUT_DURATION)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to get maritime traffic data: {e}")

# Fetch air traffic data from FastAPI
def fetch_air_traffic_data():
    """
    Fetches real-time air traffic data from the FastAPI backend.

    :return: JSON response with air traffic data
    """
    try:
        response = requests.get(f"{API_URL}/air_traffic", timeout=TIMEOUT_DURATION)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to get air traffic data: {e}")

# Display the fetched data
st.write("Maritime Traffic Data:")
maritime_data = fetch_maritime_data()
if maritime_data:
    st.write(maritime_data)

st.write("Air Traffic Data:")
air_traffic_data = fetch_air_traffic_data()
if air_traffic_data:
    st.write(air_traffic_data)
