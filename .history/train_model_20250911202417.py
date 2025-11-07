import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the data
data = pd.read_csv("pets.csv")

# Features (drop the target and PetID if not needed)
X = data.drop(columns=["PetID", "AdoptionLikelihood"])

# Target
y = data["AdoptionLikelihood"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("adoption_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")
