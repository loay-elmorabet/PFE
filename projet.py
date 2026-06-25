import requests
import json
def afficher():
#Select season:
    s=int(input("chosir une saision entre 2022,2023,2024:"))
    liste_ligues=get_leagues(s)
    # for a,v in enumerate(liste_ligues):
    #     print(a,v[1])
#Select league:
    l=int(input("chosir une league:"))
    id_ligue_choisie=liste_ligues[l][0]
    liste_team=get_teams(s,id_ligue_choisie)
    for a,v in enumerate(liste_team):
        print(a,v[1])
#Select player:
    t=int(input("chosir une équipe:"))
    id_equipe_choisie=liste_team[t][0]
    list_joueur=get_players(s,id_ligue_choisie,id_equipe_choisie)
    for a,v in enumerate(list_joueur):
        print(a,v[1])
#See stats:
    p=int(input("chosir un joueur:"))
    id_joueur_choisie=list_joueur[p][0]
    print(get_player_stats(s,id_ligue_choisie,id_equipe_choisie,id_joueur_choisie))

def secure(value):
    if(value is None):
        return 0
    else:
        return value
def diviser_safe(x1,x2):
    if(x2==0):
        return 0
    else:
        return round((x1/x2),3)

#récupérer les ligues
def get_leagues(s):
    url="https://v3.football.api-sports.io/leagues"
    api_key="d91220adabad9abc9272c4ec82b4d4ad"
    headers={"x-apisports-key":api_key}
    params={"season":s}
    response=requests.get(url,headers=headers,params=params)
    data=response.json()
    list_league=[]
    for league in data['response']:
        if(league['country']['name']in['Spain','England','France','Germany','Italy','Morocco']):
            if((league['league']['type']!='Cup') and (league['league']['name'] in ['Premier League','Bundesliga','Ligue 1','La Liga','Serie A','Botola Pro'] )):
                list_league.append((league['league']['id'],league['league']['name']))
    return list_league
#récupérer les équipes
def  get_teams(s,league_id):
    url="https://v3.football.api-sports.io/teams"
    api_key="d91220adabad9abc9272c4ec82b4d4ad"
    headers={"x-apisports-key":api_key}
    params={"season":s,"league":league_id}
    response=requests.get(url,headers=headers,params=params)
    data=response.json()
    list_team=[]
    for teams in data['response']:
        list_team.append((teams['team']['id'],teams['team']['name']))
    return list_team
#récupérer les joueurs
def get_players(s,league_id,team_id):
    url="https://v3.football.api-sports.io/players?"
    api_key="d91220adabad9abc9272c4ec82b4d4ad"
    headers={"x-apisports-key":api_key}
    params={"season":s,"league":league_id,"team":team_id}
    response=requests.get(url,headers=headers,params=params)
    data=response.json()
    list_player=[]
    for players in data['response']:
        list_player.append((players['player']['id'],players['player']['name']))
    for page in range(2,data['paging']['total']+1):
        url="https://v3.football.api-sports.io/players"
        api_key="d91220adabad9abc9272c4ec82b4d4ad"
        headers={"x-apisports-key":api_key}
        params={"season":s,"league":league_id,"team":team_id,"page":page}
        response=requests.get(url,headers=headers,params=params)
        data=response.json()
        for players in data['response']:
            list_player.append((players['player']['id'],players['player']['name']))
    return list_player
def get_player_stats(s,league_id,team_id,player_id):
    url="https://v3.football.api-sports.io/players"
    api_key="d91220adabad9abc9272c4ec82b4d4ad"
    headers={"x-apisports-key":api_key}
    params={"season":s,"league":league_id,"team":team_id,"id":player_id}
    response=requests.get(url,headers=headers,params=params)
    data=response.json()
    firstStatistic=data['response'][0]['statistics'][0]
    gamePosition=firstStatistic['games']['position']
    secondStatistic=data['response'][0]['player']
    teamName=firstStatistic['team']['name']
    playerName=secondStatistic['name']
    if (gamePosition == 'Attacker' or gamePosition == 'Forward'):
        goals=secure(firstStatistic['goals']['total'])
        shotsOn=secure(firstStatistic['shots']['on'])
        rating = secure(firstStatistic['games']['rating'])
        shotsTotal=secure(firstStatistic['shots']['total'])
        driblesSucc=secure(firstStatistic['dribbles']['success'])
        duelsWon=secure(firstStatistic['duels']['won'])
        duelsTotal=secure(firstStatistic['duels']['total'])
        gamesAppaer=secure(firstStatistic['games']['appearences'])
        IEO=diviser_safe((goals*2+shotsOn),shotsTotal) #Indice d’efficacité offensive
        IPO=diviser_safe(shotsOn,shotsTotal) #Indice de précision offensive
        IOPM=diviser_safe((goals+driblesSucc+duelsWon),gamesAppaer) #Impact offensif par match
        IDO=diviser_safe(duelsWon,duelsTotal) #Indice de domination offensive
        IGA = (IEO*0.4 + IPO*0.2 + IOPM*0.2 + IDO*0.2) #Indice global attaquant
        stats_base={
            "goals_total":goals,
            "shots_total":shotsTotal,
            "shots_on":shotsOn,
            "dribbles_success":driblesSucc,
            "duels_won":duelsWon,
            "game_rating":rating
        }
        indices={
            "IEO":IEO,
            "IPO":IPO,
            "IOPM":IOPM,
            "IDO":IDO,
            "IGA":round(IGA,3)
        }

    elif gamePosition=='Midfielder':
        goals=secure(firstStatistic['goals']['total'])
        rating=secure(firstStatistic['games']['rating'])
        keyPasses=secure(firstStatistic['passes']['key'])
        accuracyPasses=secure(firstStatistic['passes']['accuracy'])
        totalPasses=secure(firstStatistic['passes']['total'])
        tacklesInter=secure(firstStatistic['tackles']['interceptions'])
        duelsWon=secure(firstStatistic['duels']['won'])
        gamesAppaer=secure(firstStatistic['games']['appearences'])
        IC=diviser_safe(keyPasses,gamesAppaer)#Indice de création
        ICG=diviser_safe((accuracyPasses/100)*keyPasses,gamesAppaer) #Indice de contrôle du jeu
        IE=diviser_safe((keyPasses+tacklesInter),gamesAppaer)# Indice d’équilibre offensive et défensive
        IAG=diviser_safe((duelsWon+totalPasses),gamesAppaer) # Indice Activité globale
        IGM=((ICG/100)*0.3 +IC*0.25 + IE*0.2 + IAG*0.25) #Indice global milieu
        stats_base={
            "goals_total":goals,
            "passes_accuracy":accuracyPasses,
            "passes_total":totalPasses,
            "passes_key":keyPasses,
            "duels_won":duelsWon,
            "game_rating":rating
        }
        indices={
            "IC":IC,
            "ICG":ICG,
            "IE":IE,
            "IAG":IAG,
            "IGM":round(IGM,3)
        }
    elif gamePosition == 'Goalkeeper':
        goalsSaves=secure(firstStatistic['goals']['saves'])
        goalsConce=secure(firstStatistic['goals']['conceded'])
        keyPasses=secure(firstStatistic['passes']['key'])
        gamesAppaer=secure(firstStatistic['games']['appearences'])
        rating=secure(firstStatistic['games']['rating'])
        penlatySave=secure(firstStatistic['penalty']['saved'])
        IFI=diviser_safe(goalsSaves,(goalsSaves+goalsConce))#Indice de fiabilité
        IR=diviser_safe(goalsSaves,gamesAppaer)#Indice de résistance
        IS=diviser_safe(1,(goalsConce+1))#Indice de sécurité
        IGG=(IFI*0.5)+(IR*0.3)+(IS*0.2) #Indice global gardien
        stats_base={
            "penalty_saved":penlatySave,
            "goals_conceded":goalsConce,
            "passes_key":keyPasses,
            "goals_saves":goalsSaves,
            "game_rating":rating
        }
        indices={
            "IFI":IFI,
            "IR":IR,
            "IS":IS,
            "IGG":round(IGG,3)
        }

    else:
        tacklesInter=secure((firstStatistic['tackles']['interceptions']))
        tacklesTotal=secure((firstStatistic['tackles']['total']))
        duelsWon=secure(firstStatistic['duels']['won'])
        foulsComm=secure(firstStatistic['fouls']['committed'])
        duelsTotal=secure(firstStatistic['duels']['total'])
        keyPasses=secure(firstStatistic['passes']['key'])
        gamesAppaer=secure(firstStatistic['games']['appearences'])
        duelsWon=secure(firstStatistic['duels']['won'])
        rating=secure(firstStatistic['games']['rating'])
        ISD=diviser_safe((tacklesInter+duelsWon),gamesAppaer) #Indice de solidité défensive
        IDI=diviser_safe(1,(foulsComm+1))  #Indice de discipline inversée
        IDD=diviser_safe(duelsWon,duelsTotal) #Indice de domination défensive
        IPD=diviser_safe(tacklesInter,duelsTotal) #Indice Pression défensive
        IGD=(ISD*0.35 + IDD*0.25 + IDI*0.2 + IPD*0.2) #Indice globale défenseur 
        stats_base={
            "tackles_total":tacklesTotal,
            "tackles_interception":tacklesInter,
            "fouls_committed":foulsComm,
            "passes_key":keyPasses,
            "duels_won":duelsWon,
            "game_rating":rating
        }
        indices={
            "ISD":ISD,
            "IDI":IDI,
            "IDD":IDD,
            "IPD":IPD,
            "IGD":round(IGD,3)
        }
    profil_joueur={
        "nom":playerName,
        "poste":gamePosition,
        "equipe":teamName,
        "statistiques":stats_base,
        "indices_performance":indices
    }
    return profil_joueur