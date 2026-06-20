# 🏠 House Price Prediction System

<div align="center">

## 🚀 Machine Learning + Flask Web Application

A smart **House Price Prediction System** that predicts property prices using Machine Learning based on house features like area, bedrooms, bathrooms, parking availability, and house age.

**Built with ❤️ by Daya**

</div>

---

# 📌 Project Overview

The **House Price Prediction System** is a Machine Learning web application developed using **Python, Flask, Scikit-Learn, SQLite, HTML, CSS, and JavaScript**.

The system takes house details as input and predicts the estimated house price using a trained ML regression model.

It also stores prediction history and provides analytics through interactive charts.

---

# ✨ Key Highlights

⭐ Machine Learning based house price prediction  
⭐ Flask REST API backend  
⭐ Real-time prediction system  
⭐ SQLite database integration  
⭐ Prediction history tracking  
⭐ Data visualization dashboard  
⭐ Interactive charts  
⭐ Model + Scaler loading using Pickle  
⭐ Clean web interface  

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend & ML logic |
| Flask | Web framework |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Scikit-Learn | Machine Learning model |
| SQLite | Database |
| HTML/CSS/JS | Frontend |
| Pickle | Model serialization |

---

# 📂 Project Structure

```
House-Price-Prediction/

│
├── app.py                 # Flask application
│
├── train_model.py         # Model training script
│
├── generate_dataset.py    # Dataset generation
│
├── house_data.csv         # Training dataset
│
├── model.pkl              # Trained ML model
│
├── scaler.pkl             # Feature scaler
│
├── predictions.db         # SQLite database
│
├── requirements.txt       # Dependencies
│
├── static/
│   └── CSS, JS files
│
└── templates/
    └── index.html
```

---

# 🔄 System Workflow

```
        User Input
            |
            ↓
   House Details Entered
            |
            ↓
     Data Validation
            |
            ↓
   Feature Scaling
     (Scaler.pkl)
            |
            ↓
 Machine Learning Model
       (model.pkl)
            |
            ↓
   Price Prediction
            |
            ↓
 Save Result in SQLite
            |
            ↓
 Analytics Dashboard
```

---

# 🧠 Machine Learning Flow

```
Dataset
   |
   ↓
Data Cleaning
   |
   ↓
Feature Selection
   |
   ↓
Model Training
   |
   ↓
Model Evaluation
   |
   ↓
Save Model
(model.pkl)
   |
   ↓
Prediction API
```

---

# 📊 Features Used For Prediction

The model uses:

| Feature | Description |
|---|---|
| Area | House area in sq.ft |
| Bedrooms | Number of bedrooms |
| Bathrooms | Number of bathrooms |
| Parking | Parking availability |
| House Age | Age of property |

---

# 🔥 API Endpoints

## Predict House Price

```
POST /api/predict
```

Example Input:

```json
{
 "area":2500,
 "bedrooms":3,
 "bathrooms":2,
 "parking":1,
 "house_age":5
}
```

Response:

```json
{
 "success":true,
 "predicted_price":8500000
}
```

---

## Prediction History

```
GET /api/history
```

Returns previous predictions.

---

## Analytics Statistics

```
GET /api/stats
```

Provides:

- Total predictions
- Average price
- Area vs price data
- Bedroom price comparison

---

# ▶️ How To Run Project

## 1. Clone Repository

```bash
git clone https://github.com/dayanand6528/House-Price-Prediction.git
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Application

```bash
python app.py
```

---

## 4. Open Browser

```
http://127.0.0.1:5000
```

---

# 📸 Application Preview

(Add screenshots here)

Example:

```
![Home Page](screenshots/home.png)

![Dashboard](screenshots/dashboard.png)
```

---

# 📈 Future Improvements

🚀 Deploy on cloud  
🚀 Add user authentication  
🚀 Improve ML accuracy  
🚀 Add more datasets  
🚀 Add advanced visualization  
🚀 Mobile responsive UI  

---

# 👨‍💻 Developer

## Made with dedication by

# **Dayanand and with Team Members**

Machine Learning | Python | Flask Developer

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

Thank you for visiting! 🚀
