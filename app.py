import streamlit as st
import pandas as pd
import pickle
import base64
import time
from pathlib import Path

# ---------------- LOAD ----------------
model = pickle.load(open("model.pkl", "rb"))
matches = pd.read_csv("data/all_ipl_matches_data.csv")

# ---------------- TEAM DATA ----------------
TEAMS = {
    "Mumbai Indians": "assets/mi.png",
    "Chennai Super Kings": "assets/csk.png",
    "Royal Challengers Bangalore": "assets/rcb.png",
    "Kolkata Knight Riders": "assets/kkr.png",
    "Delhi Capitals": "assets/dc.png",
    "Rajasthan Royals": "assets/rr.png",
    "Sunrisers Hyderabad": "assets/srh.png",
    "Punjab Kings": "assets/pbks.png",
    "Lucknow Super Giants": "assets/lsg.png",
    "Gujarat Titans": "assets/gt.png",
}

teams = list(TEAMS.keys())

# ---------------- IMAGE ----------------
def img_to_b64(path):
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except:
        return ""

stadium_bg = img_to_b64("assets/stadium.jpg")

# ---------------- FEATURES ----------------
def win_rate(team):
    total = ((matches['team1'] == team) | (matches['team2'] == team)).sum()
    wins = (matches['match_winner'] == team).sum()
    return wins / total if total > 0 else 0.5

def recent_form(team):
    tm = matches[(matches['team1'] == team) | (matches['team2'] == team)].tail(5)
    return 0.5 if len(tm) == 0 else (tm['match_winner'] == team).mean()

# ---------------- PAGE ----------------
st.set_page_config(page_title="IPL Predictor", layout="wide")

# ---------------- CSS ----------------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{stadium_bg}");
    background-size: cover;
    background-position: center;
}}

[data-testid="stAppViewContainer"]::before {{
    content:"";
    position:fixed;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.5);
    z-index:-1;
}}

.title {{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:white;
}}
.title span {{
    color:#ffcc00;
}}

.team-card {{
    background: rgba(255,255,255,0.1);
    padding:20px;
    border-radius:15px;
    text-align:center;
    backdrop-filter: blur(10px);
    color:white;
}}

.vs {{
    text-align:center;
    font-size:40px;
    margin-top:70px;
    color:#ffcc00;
}}

.stButton>button {{
    background: linear-gradient(90deg,#ff6b00,#ffcc00);
    color:black;
    font-weight:bold;
    border-radius:10px;
}}

.result-card {{
    background:white;
    padding:30px;
    border-radius:15px;
    margin-top:20px;
}}

.bar {{
    height:12px;
    background:#eee;
    border-radius:10px;
    overflow:hidden;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">MATCH <span>PREDICTOR</span></div>', unsafe_allow_html=True)

# ---------------- TEAM SELECT ----------------
col1, col2, col3 = st.columns([4,1,4])

with col1:
    team1 = st.selectbox("Team 1", teams)
    st.markdown(f'<div class="team-card"><img src="data:image/png;base64,{img_to_b64(TEAMS[team1])}" width="80"><br><b>{team1}</b></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="vs">VS</div>', unsafe_allow_html=True)

with col3:
    team2 = st.selectbox("Team 2", teams)
    st.markdown(f'<div class="team-card"><img src="data:image/png;base64,{img_to_b64(TEAMS[team2])}" width="80"><br><b>{team2}</b></div>', unsafe_allow_html=True)

# ---------------- FIXED TOSS ----------------
# 🔥 Only allow selected teams
toss_options = [team1, team2] if team1 != team2 else [team1]

toss_winner = st.selectbox("Toss Winner", toss_options)
toss_decision = st.selectbox("Decision", ["Bat", "Field"])

# ---------------- PREDICT ----------------
if st.button("🚀 Predict Winner"):

    if team1 == team2:
        st.error("Select different teams")
    else:
        with st.spinner("Analyzing match..."):
            time.sleep(1)

        t1_wr = win_rate(team1)
        t2_wr = win_rate(team2)
        t1_form = recent_form(team1)
        t2_form = recent_form(team2)

        inp = pd.DataFrame({
            "t1_wr":[t1_wr],
            "t2_wr":[t2_wr],
            "t1_form":[t1_form],
            "t2_form":[t2_form]
        })

        prob = model.predict_proba(inp)[0]

        p1 = float(prob[1])
        p2 = float(prob[0])

        # Normalize
        total = p1 + p2
        p1 /= total
        p2 /= total

        # ✅ FIXED Toss Logic (safe)
        if toss_winner == team1:
            p1 += 0.05
        elif toss_winner == team2:
            p2 += 0.05

        # Normalize again
        total = p1 + p2
        p1 /= total
        p2 /= total

        pct1 = round(p1 * 100, 2)
        pct2 = round(p2 * 100, 2)

        winner = team1 if p1 > p2 else team2

        # ---------------- RESULT ----------------
        st.markdown(f"""
        <div class="result-card">
        <h3 style="text-align:center;">📊 Match Prediction</h3>

        <p><b>{team1}</b> - {pct1}%</p>
        <div class="bar"><div style="width:{pct1}%;background:#ff6b00;height:100%;"></div></div>

        <br>

        <p><b>{team2}</b> - {pct2}%</p>
        <div class="bar"><div style="width:{pct2}%;background:#004ba0;height:100%;"></div></div>

        <h2 style="text-align:center;margin-top:20px;">
        🏆 Winner: {winner}
        </h2>
        </div>
        """, unsafe_allow_html=True)