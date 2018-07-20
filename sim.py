#Simulator v0.1

from pymongo import MongoClient
import random

client = MongoClient('localhost', 27017)
db = client['cbb']
collection = db.get_collection('stats')

def didHappen(pct):
    return random.random() < pct

def getStats(team):
    teamCol = collection.find({'_id': '2018'})[0][team]
    return {
        'pace': float(teamCol['pace']),
        'off_rtg': float(teamCol['off_rtg']),
        'fta_per_fga_pct': float(teamCol['fta_per_fga_pct']),
        'fg3a_per_fga_pct': float(teamCol['fg3a_per_fga_pct']),
        'true_shooting_pct': float(teamCol['ts_pct']),
        'total_rebound_pct': float(teamCol['trb_pct']) / 100,
        'ast_pct': float(teamCol['ast_pct']) / 100,
        'stl_pct': float(teamCol['stl_pct']) / 100,
        'blk_pct': float(teamCol['blk_pct']) / 100,
        'effective_fg_pct': float(teamCol['efg_pct']),
        'tov_pct': float(teamCol['tov_pct']) / 100,
        'orb_pct': float(teamCol['orb_pct']) / 100,
        'ft_rate': float(teamCol['ft_rate']),
    }

def offensivePossession(fg3a_per_fga_pct, effective_fg_pct, tov_pct, orb_pct):
    if didHappen(tov_pct):
        return 'TURNOVER'
    else:
        if didHappen(fg3a_per_fga_pct):
            if didHappen(effective_fg_pct):
                return 'THREE'
            else:
                if didHappen(orb_pct):
                    return 'GOT REBOUND'
                else:
                    return 'LOST REBOUND'
        else:
            if didHappen(effective_fg_pct):
                return 'TWO'
            else:
                if didHappen(orb_pct):
                    return 'GOT REBOUND'
                else:
                    return 'LOST REBOUND'

if __name__ == '__main__':
    teamAscore = 0
    teamBscore = 0
    teamAstats = getStats('West Virginia')
    for i in range(0,70):
        print(offensivePossession(teamAstats['fg3a_per_fga_pct'], teamAstats['effective_fg_pct'],
                                  teamAstats['tov_pct'], teamAstats['orb_pct']))