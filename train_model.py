import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
def train_and_evaluate():
    print("Loading dataset...")
    df = pd.read_csv('house_data.csv')
    
    # Separate features and target
    X = df[['area_sqft', 'bedrooms', 'bathrooms', 'parking', 'house_age']]
    y = df['price']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Model (Random Forest Regressor)
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    # Evaluate
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    mae_train = mean_absolute_error(y_train, y_pred_train)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    
    
   
    
    print("\n--- Model Evaluation ---")
    print(f"Training R-squared: {r2_train:.4f}")
    print(f"Testing R-squared:  {r2_test:.4f}")
    print(f"Training MAE:       ₹{mae_train:,.2f}")
    print(f"Testing MAE:        ₹{mae_test:,.2f}")
    
    # Save the trained model and scaler
    print("\nSaving model and scaler to disk...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        
    print("Saved model.pkl and scaler.pkl successfully!")

if __name__ == '__main__':
    train_and_evaluate()
