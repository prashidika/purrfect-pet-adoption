import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib  # use joblib instead of pickle

# Load dataset
data = pd.read_csv("pets.csv")

# Features (drop PetID and target column)
X = data.drop(columns=["PetID", "AdoptionLikelihood"])

# Target column
y = data["AdoptionLikelihood"]

# Convert categorical columns to dummy variables
X = pd.get_dummies(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model using joblib
joblib.dump(model, "pet_recommender_pipeline.joblib")

print("Model trained and saved successfully!")
