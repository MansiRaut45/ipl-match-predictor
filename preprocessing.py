import pandas as pd

matches = pd.read_csv("data/all_ipl_matches_data.csv")

# Keep only valid matches
matches = matches[matches['match_winner'].notna()]

# Convert to names (IMPORTANT)
team_cols = ['team1', 'team2', 'match_winner']

for col in team_cols:
    matches[col] = matches[col].astype(str)

# ---------------- FEATURES ----------------

def get_win_rate(team, df):
    total = ((df['team1'] == team) | (df['team2'] == team)).sum()
    wins = (df['match_winner'] == team).sum()
    return wins / total if total > 0 else 0.5

def get_form(team, df):
    recent = df[((df['team1'] == team) | (df['team2'] == team))].tail(10)
    if len(recent) == 0:
        return 0.5
    wins = (recent['match_winner'] == team).sum()
    return wins / len(recent)

def get_h2h(t1, t2, df):
    h2h = df[((df['team1'] == t1) & (df['team2'] == t2)) |
             ((df['team1'] == t2) & (df['team2'] == t1))]
    if len(h2h) == 0:
        return 0.5
    wins = (h2h['match_winner'] == t1).sum()
    return wins / len(h2h)

data = []

for i, row in matches.iterrows():
    t1 = row['team1']
    t2 = row['team2']

    win1 = get_win_rate(t1, matches)
    win2 = get_win_rate(t2, matches)

    form1 = get_form(t1, matches)
    form2 = get_form(t2, matches)

    h2h_val = get_h2h(t1, t2, matches)

    data.append({
        'win_rate_diff': win1 - win2,
        'form_diff': form1 - form2,
        'h2h': h2h_val - 0.5,
        'target': 1 if row['match_winner'] == t1 else 0
    })

df = pd.DataFrame(data)

df.to_csv("data/clean_matches.csv", index=False)

print("✅ Strong dataset ready!")