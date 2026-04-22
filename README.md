# 🏏 IPL Match Winner Predictor

An AI-powered web application that predicts the winner of an IPL match using historical data, team performance, and match conditions.

---

## 📌 Project Overview

This project uses Machine Learning techniques to analyze past IPL matches and predict the winning team based on:

* Team win rate 📊
* Recent performance 🔥
* Toss outcome 🪙

The application is built with an interactive UI using Streamlit to provide real-time predictions.

---

## ✨ Features

✔ Interactive IPL-style UI
✔ Team vs Team comparison
✔ Win probability visualization
✔ Toss impact analysis
✔ Real-time prediction system
✔ Clean and responsive design

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Machine Learning:** Scikit-learn / XGBoost
* **Data Processing:** Pandas, NumPy

---

## 📂 Project Structure

```
ipl-project/
│
├── app.py                 # Streamlit web app
├── model.py               # Model training
├── preprocessing.py       # Data cleaning & feature engineering
├── model.pkl              # Trained ML model
│
├── data/
│   ├── all_ipl_matches_data.csv
│   └── clean_matches.csv
│
├── assets/                # Team logos & images
│
└── README.md
```

---

## ⚙️ How It Works

1. User selects two teams
2. Select toss winner and decision
3. Model calculates:

   * Win rate
   * Recent form
4. ML model predicts probabilities
5. UI displays winner + probability

---

## ▶️ Run Locally

```bash
git clone https://github.com/MansiRaut45/ipl-match-predictor.git
cd ipl-match-predictor

pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Dataset

* IPL historical match dataset
* Includes match results, teams, and outcomes

---

## 🎯 Future Improvements

* Add venue-based prediction
* Player-level performance analysis
* Deep learning model for higher accuracy
* Live match API integration

---

## 👩‍💻 Author

**Mansi Raut**

* GitHub: https://github.com/MansiRaut45
* LinkedIn: (https://linkedin.com/in/mansi-raut2804)

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute!

---
