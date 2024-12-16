from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Charger les données Iris
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# Entraîner le modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Sauvegarder le modèle
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Modèle sauvegardé dans 'model.pkl'")
