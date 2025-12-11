# src/Train_Model.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# -------------------------------
# 1. Paths
# -------------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "fraud_dataset_5000.csv")  # dataset in project root

print("Looking for dataset at:", data_path)

# -------------------------------
# 2. Verify Dataset
# -------------------------------
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset not found! Please check the path: {data_path}")

# -------------------------------
# 3. Load Data
# -------------------------------
df = pd.read_csv(data_path)
print("Dataset loaded successfully!")
print(df.head())
print("Columns in dataset:", df.columns.tolist())

# -------------------------------
# 3b. Ensure target is integer
# -------------------------------
if 'is_fraud' not in df.columns:
    raise KeyError("Target column 'is_fraud' not found in dataset!")
df['is_fraud'] = df['is_fraud'].astype(int)
print("Unique values in target:", df['is_fraud'].unique())

# -------------------------------
# 4. Preprocess Data
# -------------------------------
# Fill missing values
df.ffill(inplace=True)

# Encode categorical variables
df = pd.get_dummies(df, drop_first=True)

# Automatically detect numeric columns (exclude target)
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
if 'is_fraud' in numerical_features:
    numerical_features.remove('is_fraud')

print("Numeric columns to scale:", numerical_features)

# Scale numeric features
scaler = StandardScaler()
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# -------------------------------
# 5. Split Features and Target
# -------------------------------
X = df.drop('is_fraud', axis=1)
y = df['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# 6. Train Model
# -------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully!")

# -------------------------------
# 7. Evaluate Model
# -------------------------------
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# -------------------------------
# 8. Save Model
# -------------------------------
model_folder = os.path.join(script_dir, "..", "models")
model_path = os.path.join(model_folder, "trained_model.pkl")

# Ensure models folder exists
os.makedirs(model_folder, exist_ok=True)

# Save the trained model
joblib.dump(model, model_path)
print(f"Model saved successfully at {os.path.abspath(model_path)}")
