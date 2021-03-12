import pandas as pd
import numpy as np

"""
If blue team wins(1), then red team win will be 0. For such paired columns, we can combine them into one column; the value can be "blue"/"red"/"noteam"
If there is a tie (game duration will for sure smaller than 300s), the row is an outlier and will be dropped. 

KDA=(kill+assist)/death; It is usually for a single player, but in this project it will be calculated and used from a team's aspect. 
KDA is useful to combine and repersent the information from kill, assist and death. But when death=0, KDA should not be calculated(divided by 0). 
To handle such situation, we can simplely drop such rows because death=0 happens when one team is overpoweful or someone disconnected during the game. 
Such situation can be considered as outliers and should be dropped. Same thing can happend if game is too short (<16min (960s))
"""

def load_and_process(url_or_path_to_csv_file):

    # Method Chain 1 (Load data and deal with missing data)

    lol1 = (pd.read_csv('../data/raw/Master_Ranked_Games.csv')
      .rename(columns={'gameDuraton':'duration'})
      .dropna()
       )

    # Method Chain 2 (Create new columns, drop others, and do processing)

    lol2 = (lol1.assign(blueKDA=lambda x: (x['blueKills']+x['blueAssist'])/x['blueDeath'])
        .assign(redKDA=lambda x: (x['redKills']+x['redAssist'])/x['redDeath'])
        .drop(lol1[(lol1['blueDeath']==0)|(lol1['redDeath']==0)|(lol1['blueKills']==0)|(lol1['redKills']==0)|(lol1['duration']<960)].index) #drop outliers
        .assign(teamFirstBlood = lambda x: np.where(x.blueFirstBlood==1,'blue','red'))
        .assign(teamFirstTower = lambda x: np.where(x.blueFirstTower==1,'blue',(np.where(x.redFirstTower==1,'red','noTeam'))))
        .assign(teamFirstBaron = lambda x: np.where(x.blueFirstBaron==1,'blue',(np.where(x.redFirstBaron==1,'red','noTeam'))))
        .assign(teamFirstDragon = lambda x: np.where(x.blueFirstDragon==1,'blue',(np.where(x.redFirstDragon==1,'red','noTeam'))))
        .assign(teamFirstInhibitor = lambda x: np.where(x.blueFirstInhibitor==1,'blue',(np.where(x.redFirstInhibitor==1,'red','noTeam'))))
        .assign(teamWins = lambda x: np.where(x.blueWins==1,'blue','red'))
        .drop(columns={'gameId','blueWins', 'blueFirstBlood', 'blueFirstTower', 'blueFirstBaron', 'blueFirstDragon',  'blueFirstInhibitor',
                       'redWins', 'redFirstBlood', 'redFirstTower', 'redFirstBaron', 'redFirstDragon',  'redFirstInhibitor', 'blueJungleMinionKills', 
                       'redJungleMinionKills','blueKills', 'blueAssist', 'blueDeath', 'redKills', 'redAssist', 'redDeath', 
                       'blueTotalLevel', 'redTotalLevel'}) #drop now useless or no interesting columns
        .reset_index() 
        .drop(columns='index')
       )

    return lol2