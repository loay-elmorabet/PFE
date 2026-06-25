from flask import Flask , render_template, jsonify,request,session
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
@app.route('/profil')
def profil():
    saison_choisie=request.args.get('season')
    league_choisie=request.args.get('league')
    team_choisie=request.args.get('team')
    player_choisie=request.args.get('player')
    stats={}
    if saison_choisie and league_choisie and team_choisie and player_choisie:
        stats=get_player_stats(int(saison_choisie),int(league_choisie),int(team_choisie),int(player_choisie))
    return render_template('profil.html', stats=stats)

@app.route('/duel' ,methods=['GET'])
def comparer():
    saison_choisie1=request.args.get('season1')
    league_choisie1=request.args.get('league1')
    team_choisie1=request.args.get('team1')
    player_choisie1=request.args.get('player1')

    saison_choisie2=request.args.get('season2')
    league_choisie2=request.args.get('league2')
    team_choisie2=request.args.get('team2')
    player_choisie2=request.args.get('player2')

    if (saison_choisie1 and league_choisie1 and team_choisie1 and player_choisie1 and saison_choisie2 and league_choisie2 and team_choisie2 and player_choisie2):
        stats_p1=get_player_stats(int(saison_choisie1),int(league_choisie1),int(team_choisie1),int(player_choisie1))
        stats_p2=get_player_stats(int(saison_choisie2),int(league_choisie2),int(team_choisie2),int(player_choisie2))
        position_p1=stats_p1['poste']
        position_p2=stats_p2['poste']
        if(position_p1!=position_p2):
            return f"Décalage détecté ! Poste J1 reçu: '{position_p1}' (Type: {type(position_p1)}) | Poste J2 calculé: '{position_p2}' (Type: {type(position_p2)})"
        return render_template('rival.html', stats1=stats_p1, stats2=stats_p2)
    return render_template('duel.html')
@app.route('/accueil')
def accueil():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)