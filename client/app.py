# libraries
import streamlit as st
import requests
import numpy as np
import os
import sys
import importlib
from datetime import datetime 

# Add the server folder to the path
server_path = os.path.join(os.path.dirname(__file__), "server")
if server_path not in sys.path:
    sys.path.append(server_path)

# Import the modules
try:
    import train
except ModuleNotFoundError:
    raise ModuleNotFoundError(f"Unable to find the 'train' module. Check if the path {server_path} is correct.")

importlib.reload(train)
from train import training_page
from metrics import show_metrics
from predict import predict_page
from metrics import show_metrics
from home import home_page

# Page configuration
st.set_page_config(
    page_title="Iris Flower Prediction",
    page_icon="🌸",
    layout="centered",
)

# Tabs configuration
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🤖 Training Models", "🔮 Predict", "📊 Metrics"])

# Home Page
with tab1:
    home_page()

# Training Models Page
with tab2:
    training_page()

# Predict Page
with tab3:
    predict_page()

# Metrics Page
with tab4:
    show_metrics()
