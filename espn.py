from espn_api.football import League
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

swid = "insert here"
espn_s2 = "insert here"
league = League(league_id=16542287, year=2020, espn_s2=espn_s2, swid=swid)
# print(league.teams)
# print(league.power_rankings(week=13))
# print(f"Top scorer; {league.top_scorer()}")
# print(f"Least scorer; {league.least_scorer()}")
settings = league.settings
week_number = settings.reg_season_count
teams_number = settings.team_count
matchups_in_week = int(teams_number / 2)

team = league.teams[0]
# print(team)
# print(team.wins)
# print(team.losses)
complete_weeks = (team.wins + team.losses) + 1


def clean_team_name(name):
    cleaned_name = name[5:-1]
    return cleaned_name


scores = []
for week in range(1, complete_weeks):
    print(f"Week {week}")
    box_scores = league.box_scores(week)
    for matchup in range(matchups_in_week):
        home_win = "Win" if box_scores[matchup].home_score > box_scores[matchup].away_score else "Loss"
        away_win = "Win" if box_scores[matchup].away_score > box_scores[matchup].home_score else "Loss"
        home_team = clean_team_name(str(box_scores[matchup].home_team))
        away_team = clean_team_name(str(box_scores[matchup].away_team))
        scores.append([week, home_team, box_scores[matchup].home_score, home_win])
        scores.append([week, away_team, box_scores[matchup].away_score, away_win])
        print(f"Matchup: {matchup + 1} : {home_team} ({away_team} points)"
              f"vs {box_scores[matchup].away_team} - ({box_scores[matchup].away_score} points)")

df = pd.DataFrame(scores, columns=['Week', 'Name', 'Score', 'Win?'])
print(df)
df.to_csv(r"data\ffdata.csv")

df = pd.read_csv(r'data\ffdata.csv')

fig, ax = plt.subplots(1, 1, figsize=(16, 6))
sns.violinplot(x='Name', y='Score',
               data=df,
               width=1,
               split=True,
               linewidth=2,
               # Removes the infinity - sticks to 0 axis
               # cut=0
               # palette='muted',
               # order=list('ABCDEFGHIJ')
               )
ax.set_xlabel('')
ax.set_title('Distribution of score, ordered by final standing')
plt.show()


fig, ax = plt.subplots(1, 1, figsize=(16, 6))
sns.violinplot(x='Name', y='Score',
               data=df,
               width=1,
               hue="Win?",
               split=True,
               inner="stick",
               scale_hue=False,
               bw=.5,
               palette="Set2",
               scale="count",
               linewidth=2,
               )
ax.set_xlabel('')
ax.set_title('Distribution of score, ordered by final standing')
plt.show()
