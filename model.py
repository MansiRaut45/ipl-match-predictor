import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv("data/all_ipl_matches_data.csv")

data = data[data['match_winner'].notna()]

# ---------------- FEATURES ----------------

def win_rate(team, df):
    total = ((df['team1'] == team) | (df['team2'] == team)).sum()
    wins = (df['match_winner'] == team).sum()
    return wins / total if total > 0 else 0.5

def form(team, df):
    recent = df[((df['team1'] == team) | (df['team2'] == team))].tail(10)
    if len(recent) == 0:
        return 0.5
    return (recent['match_winner'] == team).mean()

rows = []

for _, row in data.iterrows():
    t1 = row['team1']
    t2 = row['team2']

    rows.append({
        "t1_wr": win_rate(t1, data),
        "t2_wr": win_rate(t2, data),
        "t1_form": form(t1, data),
        "t2_form": form(t2, data),
        "target": 1 if row['match_winner'] == t1 else 0
    })

df = pd.DataFrame(rows)

X = df[['t1_wr', 't2_wr', 't1_form', 't2_form']]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = XGBClassifier(
    n_estimators=400,
    max_depth=6,
    learning_rate=0.05
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))

pickle.dump(model, open("model.pkl", "wb"))

print("✅ FINAL MODEL READY")