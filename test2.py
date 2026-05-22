import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
s=int(input("chosir une saision entre 2022,2023,2024:"))
url="https://v3.football.api-sports.io/leagues?season=2022"
api_key="d91220adabad9abc9272c4ec82b4d4ad"
headers={"x-apisports-key":api_key}
params={"season":s}
response=requests.get(url,headers=headers,params=params)
data1=response.json()
list_league=[]
for league in data1['response']:
        if(league['country']['name']in['Spain','England','France','Germany','Italy','Morocco']):
            if((league['league']['type']!='Cup') and (league['league']['name'] in ['Premier League','Bundesliga','Ligue 1','La Liga','Serie A','Botola Pro'] )):
                list_league.append((league['league']['id'],league['league']['name']))
for a,v in enumerate(list_league):
    print(a,v[1])
l=int(input("chosir une league:"))
league_id=list_league[l]
url="https://v3.football.api-sports.io/teams?season=2022&league=league_id"
api_key="d91220adabad9abc9272c4ec82b4d4ad"
headers={"x-apisports-key":api_key}
params={"season":s,"league":league_id[0]}
response=requests.get(url,headers=headers,params=params)
data2=response.json()
list_team=[]
for teams in data2['response']:
    list_team.append((teams['team']['id'],teams['team']['name']))
for a,v in enumerate(list_team):
    print(a,v[1])
t=int(input("chosir une équipe:"))
team_id=list_team[t]
print(team_id)
page=0
url="https://v3.football.api-sports.io/players?season=2022&league=league_id&team=team_id"
api_key="d91220adabad9abc9272c4ec82b4d4ad"
headers={"x-apisports-key":api_key}
params={"season":s,"league":league_id[0],"team":team_id[0]}
response=requests.get(url,headers=headers,params=params)
data3=response.json()
list_player=[]
for page in range(1,data3['paging']['total']+1):
    url="https://v3.football.api-sports.io/players?season=2022&league=league_id&team=team_id&page=page"
    api_key="d91220adabad9abc9272c4ec82b4d4ad"
    headers={"x-apisports-key":api_key}
    params={"season":s,"league":league_id[0],"team":team_id[0],"page":page}
    response=requests.get(url,headers=headers,params=params)
    data3=response.json()
    for players in data3['response']:
        list_player.append((players['player']['id'],players['player']['name']))
for a,v in enumerate(list_player):
    print(a,v[1])
p=int(input("chosir un joueur:"))
player_id=list_player[p]
url="https://v3.football.api-sports.io/players?season=2022&league=league_id&team=team_id"
api_key="d91220adabad9abc9272c4ec82b4d4ad"
headers={"x-apisports-key":api_key}
params={"season":s,"league":league_id[0],"team":team_id[0],"id":player_id[0]}
response=requests.get(url,headers=headers,params=params)
data4=response.json()
firstStatistic=data4['response'][0]['statistics'][0]
gamePosition=firstStatistic['games']['position']
secondStatistic=data4['response'][0]['player']
playerName=secondStatistic['name']
if(player_id[1]==playerName):
    if (gamePosition == 'Attacker' or gamePosition == 'Forward'):
        df_stats=pd.json_normalize(data4['response'][0]['statistics'])
        IEO=(firstStatistic['goals']['total']*2+firstStatistic['shots']['on'])/firstStatistic['shots']['total']  #Indice d’efficacité offensive
        IPO=firstStatistic['shots']['on']/firstStatistic['shots']['total'] #Indice de précision offensive
        IOPM=(firstStatistic['goals']['total']+firstStatistic['dribbles']['success']+firstStatistic['duels']['won'])/firstStatistic['games']['appearences'] #Impact offensif par match
        IDO=firstStatistic['duels']['won']/firstStatistic['duels']['total'] #Indice de domination offensive
        IGA = (IEO*0.4 + IPO*0.2 + IOPM*0.2 + IDO*0.2) #Indice global attaquant 
        indicateurs = ["IEO", "IPO", "IOPM", "IDO"]
        values = [IEO, IPO, IOPM, IDO]
        print("Nom :",playerName)
        print("Pote :",gamePosition)
        print(df_stats[['team.name', 'goals.total', 'games.rating','shots.total','shots.on','dribbles.success', 'duels.won']])
        print("efficacité offensive :",round(IEO,3))
        print("précision offensive : ",round(IPO,3))
        print("Impact offensif par match : ",round(IOPM,3))
        print("domination offensive : ",round(IDO,3))
        plt.bar(indicateurs,values)
        plt.title('Attaque')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGA>=1.2): 
            print("Le score du attaquant est Excellent")
        elif(IGA>=0.8 and IGA<1.2):
            print("Le score du attaquant est Bon")
        elif(IGA>=0.4 and IGA<0.8):
            print("Le score du attaquant est Moyen")
        else:
            print("Le score du attaquant est Faible")
    elif gamePosition=='Midfielder':
        df_stats=pd.json_normalize(data4['response'][0]['statistics'])
        IC=firstStatistic['passes']['key']/firstStatistic['games']['appearences'] #Indice de création
        ICG=firstStatistic['passes']['accuracy']*firstStatistic['passes']['key'] #Indice de contrôle du jeu
        IE=(firstStatistic['passes']['key']+firstStatistic['tackles']['interceptions'])/firstStatistic['games']['appearences'] # Indice d’équilibre offensive et défensive
        IAG=(firstStatistic['duels']['won']+firstStatistic['passes']['total'])/firstStatistic['games']['appearences'] #Activité globale
        IGM=((ICG/100)*0.3 +IC*0.25 + IE*0.2 + IAG*0.25) #Indice global milieu
        indicateurs = ["IC", "ICG", "IE", "IAG"]
        values = [IC, ICG, IE, IAG]
        print(df_stats[['team.name', 'goals.total', 'games.rating','tackles.interceptions','passes.accuracy','passes.key', 'duels.won']])
        print("création du jeu :",round(IC,3))
        print("contrôle du jeu : ",round(ICG,3))
        print("équilibre offensive et défensive : ",round(IE,3))
        print("Activité globale : ",round(IAG,3))
        plt.bar(indicateurs,values)
        plt.title('milieu')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGM>=1.5): 
            print("Le score du milieu est Excellent")
        elif(IGM>=1.0 and IGM<1.5):
            print("Le score du milieu est Bon")
        elif(IGM>=0.5 and IGM<1.0):
            print("Le score du milieu est Moyen")
        else:
            print("Le score du milieu est Faible")
    elif gamePosition == 'Goalkeeper':
        df_stats=pd.json_normalize(data4['response'][0]['statistics'])
        IFI=firstStatistic['goals']['saves']/(firstStatistic['goals']['saves'])+(firstStatistic['goals']['conceded']) #Indice de fiabilité
        IR=firstStatistic['goals']['saves']/firstStatistic['games']['appearences'] #Indice de résistance
        IS=1/(firstStatistic['goals']['conceded']+1) #Indice de sécurité
        IGG=(IFI*0.5)+(IR*0.3)+(IS*0.2) #Indice global gardien 
        indicateurs = ["IFI", "IR", "IS", "IGG"]
        values = [IFI, IR, IS, IGG]
        print(df_stats[['team.name', 'goals.total', 'games.rating','goals.conceded','goals.saves']])
        print("fiabilité :",round(IFI,3))
        print("résistance : ",round(IR,3))
        print("sécurité : ",round(IS,3))
        print("score du gardien : ",round(IGG,3))
        plt.bar(indicateurs,values)
        plt.title('gardien')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGG>=0.8): 
            print("Le score du gardien est Excellent")
        elif(IGG>=0.6 and IGG<0.8):
            print("Le score du gardien est Bon")
        elif(IGG>=0.4 and IGG<0.6):
            print("Le score du gardien est Moyen")
        else:
            print("Le score du gardien est Faible")
    else:
        df_stats=pd.json_normalize(data4['response'][0]['statistics'])
        ISD=(firstStatistic['tackles']['interceptions'] + firstStatistic['duels']['won'])/firstStatistic['games']['appearences'] #Indice de solidité défensive
        IDI=1/(firstStatistic['fouls']['committed']+1) #Indice de discipline inversée
        IDD=firstStatistic['duels']['won']/firstStatistic['duels']['total'] #Indice de domination défensive
        IPD=firstStatistic['tackles']['interceptions']/firstStatistic['duels']['total'] #Indice Pression défensive
        IGD=(ISD*0.35 + IDD*0.25 + IDI*0.2 + IPD*0.2)
        indicateurs = ["ISD", "IDI", "IPD", "IGD"]
        values = [ISD, IDI, IPD, IGD]
        print(df_stats[['team.name', 'tackles.total','tackles.interceptions','fouls.committed','passes.key', 'duels.won','games.rating']])
        print("solidité défensive:",round(ISD,3))
        print("discipline inversée : ",round(IDI,3))
        print("domination défensive : ",round(IDD,3))
        print("Pression défensive : ",round(IPD,3))
        plt.bar(indicateurs,values)
        plt.title('Défense')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGD>=1.0): 
            print("Le score du défenseur est Excellent")
        elif(IGD>=0.7 and IGD<1.0):
            print("Le score du défenseur est Bon")
        elif(IGD>=0.4 and IGD<0.7):
            print("Le score du défenseur est Moyen")
        else:
            print("Le score du défenseur est Faible")
else:
    print("no player with that name")
for page in range(1,data3['paging']['total']+1):
    url="https://v3.football.api-sports.io/players?season=2022&league=league_id&team=team_id&page=page"
    api_key="d91220adabad9abc9272c4ec82b4d4ad"
    headers={"x-apisports-key":api_key}
    params={"season":s,"league":league_id[0],"team":team_id[0],"page":page}
    response=requests.get(url,headers=headers,params=params)
    data3=response.json()
    for players in data3['response']:
        list_player.append((players['player']['id'],players['player']['name']))
for a,v in enumerate(list_player):
    print(a,v[1])
p2=int(input("chosir 2eme  joueur:"))
player_id2=list_player[p2]
url="https://v3.football.api-sports.io/players?season=2022&league=league_id&team=team_id"
api_key="d91220adabad9abc9272c4ec82b4d4ad"
headers={"x-apisports-key":api_key}
params={"season":s,"league":league_id[0],"team":team_id[0],"id":player_id2[0]}
response=requests.get(url,headers=headers,params=params)
data5=response.json()
firstStatistic2=data5['response'][0]['statistics'][0]
gamePosition2=firstStatistic2['games']['position']
secondStatistic2=data5['response'][0]['player']
playerName2=secondStatistic2['name']
if(player_id2[1]==playerName2):
    if (gamePosition2 == 'Attacker' or gamePosition2 == 'Forward'):
        df_stats=pd.json_normalize(data5['response'][0]['statistics'])
        IEO2=(firstStatistic2['goals']['total']*2+firstStatistic2['shots']['on'])/firstStatistic2['shots']['total']  #Indice d’efficacité offensive
        IPO2=firstStatistic2['shots']['on']/firstStatistic2['shots']['total'] #Indice de précision offensive
        IOPM2=(firstStatistic2['goals']['total']+firstStatistic2['dribbles']['success']+firstStatistic2['duels']['won'])/firstStatistic2['games']['appearences'] #Impact offensif par match
        IDO2=firstStatistic2['duels']['won']/firstStatistic2['duels']['total'] #Indice de domination offensive
        IGA2 = (IEO2*0.4 + IPO2*0.2 + IOPM2*0.2 + IDO2*0.2) #Indice global attaquant 
        indicateurs2 = ["IEO2", "IPO2", "IOPM2", "IDO2"]
        values2 = [IEO2, IPO2, IOPM2, IDO2]
        print("Nom :",playerName)
        print("Pote :",gamePosition)
        print(df_stats[['team.name', 'goals.total', 'games.rating','shots.total','shots.on','dribbles.success', 'duels.won']])
        print("efficacité offensive :",round(IEO2,3))
        print("précision offensive : ",round(IPO2,3))
        print("Impact offensif par match : ",round(IOPM2,3))
        print("domination offensive : ",round(IDO2,3))
        plt.bar(indicateurs,values)
        plt.title('Attaque')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGA2>=1.2): 
            print("Le score du attaquant est Excellent")
        elif(IGA2>=0.8 and IGA2<1.2):
            print("Le score du attaquant est Bon")
        elif(IGA2>=0.4 and IGA2<0.8):
            print("Le score du attaquant est Moyen")
        else:
            print("Le score du attaquant est Faible")
    elif gamePosition=='Midfielder':
        df_stats=pd.json_normalize(data5['response'][0]['statistics'])
        IC=firstStatistic['passes']['key']/firstStatistic['games']['appearences'] #Indice de création
        ICG=firstStatistic['passes']['accuracy']*firstStatistic['passes']['key'] #Indice de contrôle du jeu
        IE=(firstStatistic['passes']['key']+firstStatistic['tackles']['interceptions'])/firstStatistic['games']['appearences'] # Indice d’équilibre offensive et défensive
        IAG=(firstStatistic['duels']['won']+firstStatistic['passes']['total'])/firstStatistic['games']['appearences'] #Activité globale
        IGM=((ICG/100)*0.3 +IC*0.25 + IE*0.2 + IAG*0.25) #Indice global milieu
        indicateurs = ["IC", "ICG", "IE", "IAG"]
        values = [IC, ICG, IE, IAG]
        print(df_stats[['team.name', 'goals.total', 'games.rating','tackles.interceptions','passes.accuracy','passes.key', 'duels.won']])
        print("création du jeu :",round(IC,3))
        print("contrôle du jeu : ",round(ICG,3))
        print("équilibre offensive et défensive : ",round(IE,3))
        print("Activité globale : ",round(IAG,3))
        plt.bar(indicateurs,values)
        plt.title('milieu')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGM>=1.5): 
            print("Le score du milieu est Excellent")
        elif(IGM>=1.0 and IGM<1.5):
            print("Le score du milieu est Bon")
        elif(IGM>=0.5 and IGM<1.0):
            print("Le score du milieu est Moyen")
        else:
            print("Le score du milieu est Faible")
    elif gamePosition == 'Goalkeeper':
        df_stats=pd.json_normalize(data5['response'][0]['statistics'])
        IFI=firstStatistic['goals']['saves']/(firstStatistic['goals']['saves'])+(firstStatistic['goals']['conceded']) #Indice de fiabilité
        IR=firstStatistic['goals']['saves']/firstStatistic['games']['appearences'] #Indice de résistance
        IS=1/(firstStatistic['goals']['conceded']+1) #Indice de sécurité
        IGG=(IFI*0.5)+(IR*0.3)+(IS*0.2) #Indice global gardien 
        indicateurs = ["IFI", "IR", "IS", "IGG"]
        values = [IFI, IR, IS, IGG]
        print(df_stats[['team.name', 'goals.total', 'games.rating','goals.conceded','goals.saves']])
        print("fiabilité :",round(IFI,3))
        print("résistance : ",round(IR,3))
        print("sécurité : ",round(IS,3))
        print("score du gardien : ",round(IGG,3))
        plt.bar(indicateurs,values)
        plt.title('gardien')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGG>=0.8): 
            print("Le score du gardien est Excellent")
        elif(IGG>=0.6 and IGG<0.8):
            print("Le score du gardien est Bon")
        elif(IGG>=0.4 and IGG<0.6):
            print("Le score du gardien est Moyen")
        else:
            print("Le score du gardien est Faible")
    else:
        df_stats=pd.json_normalize(data5['response'][0]['statistics'])
        ISD=(firstStatistic['tackles']['interceptions'] + firstStatistic['duels']['won'])/firstStatistic['games']['appearences'] #Indice de solidité défensive
        IDI=1/(firstStatistic['fouls']['committed']+1) #Indice de discipline inversée
        IDD=firstStatistic['duels']['won']/firstStatistic['duels']['total'] #Indice de domination défensive
        IPD=firstStatistic['tackles']['interceptions']/firstStatistic['duels']['total'] #Indice Pression défensive
        IGD=(ISD*0.35 + IDD*0.25 + IDI*0.2 + IPD*0.2)
        indicateurs = ["ISD", "IDI", "IPD", "IGD"]
        values = [ISD, IDI, IPD, IGD]
        print(df_stats[['team.name', 'tackles.total','tackles.interceptions','fouls.committed','passes.key', 'duels.won','games.rating']])
        print("solidité défensive:",round(ISD,3))
        print("discipline inversée : ",round(IDI,3))
        print("domination défensive : ",round(IDD,3))
        print("Pression défensive : ",round(IPD,3))
        plt.bar(indicateurs,values)
        plt.title('Défense')
        plt.xlabel('indicateurs')
        plt.ylabel('values')
        plt.show()
        if(IGD>=1.0): 
            print("Le score du défenseur est Excellent")
        elif(IGD>=0.7 and IGD<1.0):
            print("Le score du défenseur est Bon")
        elif(IGD>=0.4 and IGD<0.7):
            print("Le score du défenseur est Moyen")
        else:
            print("Le score du défenseur est Faible")
else:
    print("no player with that name")
if(gamePosition==gamePosition2):
    if(IGA>IGA2):
        print(playerName," est meileur concernat le global attaquant ")
    else:
        print(playerName2," est meileur concernat le global attaquant ")
    indicateurs = ["IEO", "IPO", "IOPM", "IDO"]
    values = [IEO, IPO, IOPM, IDO]
    indicateurs2 = ["IEO2", "IPO2", "IOPM2", "IDO2"]
    values2 = [IEO2, IPO2, IOPM2, IDO2]
    plt.bar(indicateurs,values,color='r')
    plt.bar(indicateurs2,values2,color='b')
    plt.xlabel('indicateurs')
    plt.ylabel('values')
    plt.show()