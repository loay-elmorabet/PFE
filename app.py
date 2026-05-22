from flask import Flask , render_template, jsonify,request
from projet import get_player_stats,get_leagues,get_teams,get_players
app = Flask(__name__)

@app.route('/joueur')
def index():
    return render_template('index.html')
@app.route('/api/leagues')
def league():
    saison_choisie=request.args.get('season')
    print("La saison reçue par Flask est :", saison_choisie)
    l=[]
    if saison_choisie:
        l=get_leagues(int(saison_choisie))

    return jsonify(l)

@app.route('/api/leagues/teams')
def team():
    saison_choisie=request.args.get('season')
    league_choisie=request.args.get('league')
    t=[]
    if saison_choisie and league_choisie:
        t=get_teams(int(saison_choisie),int(league_choisie))
    return jsonify(t)
@app.route('/api/leagues/teams/players')
def player():
    saison_choisie=request.args.get('season')
    league_choisie=request.args.get('league')
    team_choisie=request.args.get('team')
    p=[]
    if saison_choisie and league_choisie and team_choisie:
        p=get_players(int(saison_choisie),int(league_choisie),int(team_choisie))
    return jsonify(p)


if __name__ == '__main__':
    app.run(debug=True)