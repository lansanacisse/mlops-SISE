import os
import pickle
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Create the directory to save models
def create_models_dir():
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    return models_dir

# Load a dataset
def load_dataset(file_path):
    # Convert the path to an absolute path
    abs_path = os.path.abspath(file_path)
    
    if not os.path.exists(abs_path):
        st.error(f"The file {abs_path} does not exist.")
        return None
    
    data = pd.read_csv(abs_path)
    return data

# Train the model
def train_model(algorithm, X_train, y_train, params):
    if algorithm == "Random Forest":
        model = RandomForestClassifier(**params)
    elif algorithm == "SVM":
        model = SVC(**params, probability=True)
    elif algorithm == "Decision Tree":
        model = DecisionTreeClassifier(**params)
    elif algorithm == "XGBoost":
        model = XGBClassifier(**params, use_label_encoder=False, eval_metric="logloss")
    else:
        st.error("Unsupported algorithm.")
        return None

    model.fit(X_train, y_train)
    return model

# Save the model
def save_model(model, algorithm_name, models_dir):
    model_path = os.path.join(models_dir, f"{algorithm_name}_model.pkl")
    with open(model_path, "wb") as file:
        pickle.dump(model, file)
    return model_path

# User interface for training configuration
def training_page():
    st.title("Model Training")

    # Use an absolute path based on Docker
    dataset_path = "/app/data/Iris.csv"
    data = load_dataset(dataset_path)

    if data is not None:
        st.write("Data Preview:", data.head())

        # Select the target column and feature columns
        target_column = st.selectbox("Target Column", data.columns)
        feature_columns = st.multiselect("Feature Columns", [col for col in data.columns if col != target_column])

        if target_column and feature_columns:
            X = data[feature_columns]
            y = data[target_column]

            # Encode target classes for XGBoost
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)

            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Select an algorithm
            algorithm = st.selectbox(
                "Choose an Algorithm",
                ["Random Forest", "SVM", "Decision Tree", "XGBoost"]
            )

            # Configure hyperparameters in the main form
            params = {}
            if algorithm == "Random Forest":
                st.subheader("Hyperparameters for Random Forest")
                params["n_estimators"] = st.slider("Number of Estimators", 10, 500, 100)
                params["max_depth"] = st.slider("Max Depth", 1, 20, 5)
            elif algorithm == "SVM":
                st.subheader("Hyperparameters for SVM")
                params["C"] = st.slider("C (Regularization)", 0.01, 10.0, 1.0)
                params["kernel"] = st.selectbox("Kernel", ["linear", "rbf", "poly"])
            elif algorithm == "Decision Tree":
                st.subheader("Hyperparameters for Decision Tree")
                params["max_depth"] = st.slider("Max Depth", 1, 20, 5)
            elif algorithm == "XGBoost":
                st.subheader("Hyperparameters for XGBoost")
                params["learning_rate"] = st.slider("Learning Rate", 0.01, 0.5, 0.1)
                params["n_estimators"] = st.slider("Number of Estimators", 10, 500, 100)

            # Button to train the model
            if st.button("Train Model"):
                model = train_model(algorithm, X_train, y_train, params)

                if model:
                    # Save the model
                    models_dir = create_models_dir()
                    model_path = save_model(model, algorithm.replace(" ", "_"), models_dir)

                    # Evaluate the model
                    y_pred = model.predict(X_test)
                    accuracy = accuracy_score(y_test, y_pred)

                    st.success(f"Model trained successfully and saved in the Models folder.")
                else:
                    st.error("Model training failed.")
