import os
import sqlite3
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Paths to ML files
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'
DATABASE_PATH = 'predictions.db'

# Load the trained model and scaler
if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
else:
    raise FileNotFoundError("Model or Scaler not found! Run train_model.py first.")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area REAL NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            parking INTEGER NOT NULL,
            house_age REAL NOT NULL,
            predicted_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    # Seed database with initial predictions if empty
    cursor.execute('SELECT COUNT(*) FROM predictions')
    count = cursor.fetchone()[0]
    if count == 0:
        import random
        print("Seeding database with initial records for analytics visualization...")
        # Create 15 properties scattered over the last 15 days
        for _ in range(15):
            area = float(random.randint(700, 3800))
            # Correlate features similarly to the generator
            bedrooms = int(np.clip(np.round(area / 900 + random.normalvariate(0.2, 0.7)), 1, 5))
            bathrooms = int(np.clip(np.round(bedrooms * 0.8 + random.normalvariate(0.1, 0.5)), 1, 4))
            parking = random.choice([0, 1])
            house_age = float(random.randint(0, 45))
            
            features = pd.DataFrame(
                [[area, bedrooms, bathrooms, parking, house_age]], 
                columns=['area_sqft', 'bedrooms', 'bathrooms', 'parking', 'house_age']
            )
            features_scaled = scaler.transform(features)
            pred = model.predict(features_scaled)[0]
            pred = max(float(pred), 2000000.0)
            
            days_offset = random.randint(1, 15)
            hours_offset = random.randint(1, 23)
            minutes_offset = random.randint(1, 59)
            
            cursor.execute('''
                INSERT INTO predictions (area, bedrooms, bathrooms, parking, house_age, predicted_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now', '-{} days', '-{} hours', '-{} minutes'))
            '''.format(days_offset, hours_offset, minutes_offset), (area, bedrooms, bathrooms, parking, house_age, pred))
        conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Extract and validate fields
        try:
            area = float(data.get('area'))
            bedrooms = int(data.get('bedrooms'))
            bathrooms = int(data.get('bathrooms'))
            parking = int(data.get('parking'))  # 0 or 1
            house_age = float(data.get('house_age'))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid data types. Please check your inputs.'}), 400
        
        if area <= 0 or bedrooms <= 0 or bathrooms <= 0 or house_age < 0:
            return jsonify({'error': 'Input values must be positive and realistic.'}), 400
        
        if parking not in [0, 1]:
            return jsonify({'error': 'Parking availability must be 0 (No) or 1 (Yes).'}), 400

        # Scale features
        features = pd.DataFrame(
            [[area, bedrooms, bathrooms, parking, house_age]], 
            columns=['area_sqft', 'bedrooms', 'bathrooms', 'parking', 'house_age']
        )
        features_scaled = scaler.transform(features)
        
        # Predict price
        prediction = model.predict(features_scaled)[0]
        # Keep price realistic
        prediction = max(float(prediction), 2000000.0)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (area, bedrooms, bathrooms, parking, house_age, predicted_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (area, bedrooms, bathrooms, parking, house_age, prediction))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'predicted_price': round(prediction, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Retrieve last 50 entries
        cursor.execute('''
            SELECT area, bedrooms, bathrooms, parking, house_age, predicted_price, created_at
            FROM predictions
            ORDER BY id DESC
            LIMIT 50
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for r in rows:
            # Format date representation nicely
            dt_obj = datetime.strptime(r['created_at'], '%Y-%m-%d %H:%M:%S')
            formatted_date = dt_obj.strftime('%b %d, %Y %I:%M %p')
            
            history.append({
                'area': r['area'],
                'bedrooms': r['bedrooms'],
                'bathrooms': r['bathrooms'],
                'parking': 'Yes' if r['parking'] == 1 else 'No',
                'house_age': r['house_age'],
                'predicted_price': round(r['predicted_price'], 2),
                'created_at': formatted_date
            })
            
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Basic Stats
        cursor.execute('SELECT COUNT(*), AVG(predicted_price) FROM predictions')
        count, avg_price = cursor.fetchone()
        count = count or 0
        avg_price = round(avg_price, 2) if avg_price else 0.0
        
        # 2. Scatter Plot Data (Area vs Predicted Price)
        cursor.execute('SELECT area, predicted_price FROM predictions ORDER BY id DESC LIMIT 100')
        scatter_rows = cursor.fetchall()
        scatter_data = [{'x': r['area'], 'y': round(r['predicted_price'], 2)} for r in scatter_rows]
        
        # 3. Bar Chart Data (Average Price by Bedrooms)
        cursor.execute('''
            SELECT bedrooms, AVG(predicted_price) as avg_p 
            FROM predictions 
            GROUP BY bedrooms 
            ORDER BY bedrooms
        ''')
        bar_rows = cursor.fetchall()
        bar_labels = [int(r['bedrooms']) for r in bar_rows]
        bar_values = [round(r['avg_p'], 2) for r in bar_rows]
        
        conn.close()
        
        return jsonify({
            'total_predictions': count,
            'average_price': avg_price,
            'scatter_data': scatter_data,
            'bar_data': {
                'labels': bar_labels,
                'values': bar_values
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run server on port 5000
    app.run(debug=True, port=5000)
