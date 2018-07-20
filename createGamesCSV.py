import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['cbb']
collection = db.get_collection('stats').find({'_id': '2018'})

teamName = []
opponent = []
location = []
result = []
pts = []
pts_against = []

team_fg = []
team_fga = []
team_fg_pct = []
team_fg2 = []
team_fg2a = []
team_fg2_pct = []
team_fg3 = []
team_fg3a = []
team_fg3_pct = []
team_ft = []
team_fta = []
team_ft_pct = []
team_ast = []
team_pts = []
team_pts_per_g = []
team_orb = []
team_drb = []
team_trb = []
team_stl = []
team_blk = []
team_tov = []

opp_fg = []
opp_fga = []
opp_fg_pct = []
opp_fg2 = []
opp_fg2a = []
opp_fg2_pct = []
opp_fg3 = []
opp_fg3a = []
opp_fg3_pct = []
opp_ft = []
opp_fta = []
opp_ft_pct = []
opp_ast = []
opp_pts = []
opp_pts_per_g = []
opp_orb = []
opp_drb = []
opp_trb = []
opp_stl = []
opp_blk = []
opp_tov = []

team2_team_fg = []
team2_team_fga = []
team2_team_fg_pct = []
team2_team_fg2 = []
team2_team_fg2a = []
team2_team_fg2_pct = []
team2_team_fg3 = []
team2_team_fg3a = []
team2_team_fg3_pct = []
team2_team_ft = []
team2_team_fta = []
team2_team_ft_pct = []
team2_team_ast = []
team2_team_pts = []
team2_team_pts_per_g = []
team2_team_orb = []
team2_team_drb = []
team2_team_trb = []
team2_team_stl = []
team2_team_blk = []
team2_team_tov = []

team2_opp_fg = []
team2_opp_fga = []
team2_opp_fg_pct = []
team2_opp_fg2 = []
team2_opp_fg2a = []
team2_opp_fg2_pct = []
team2_opp_fg3 = []
team2_opp_fg3a = []
team2_opp_fg3_pct = []
team2_opp_ft = []
team2_opp_fta = []
team2_opp_ft_pct = []
team2_opp_ast = []
team2_opp_pts = []
team2_opp_pts_per_g = []
team2_opp_orb = []
team2_opp_drb = []
team2_opp_trb = []
team2_opp_stl = []
team2_opp_blk = []
team2_opp_tov = []

data = {}

for year in collection:
    for team in year:
        if team != '_id':
            for date in year[team]['games']:
                # Excluding tourney games for predictive testing. Erase try and if blocks to include
                try:
                    if year[team]['games'][date]['game_type'] == 'NCAA':
                        try:
                            # Get team name
                            teamNameStat = team

                            # Get game Stats
                            gameInfo = year[team]['games'][date]
                            opponentStat = gameInfo['opp_name']
                            locationStat = gameInfo['game_location']
                            resultStat = gameInfo['game_result']
                            ptsStat = gameInfo['pts']
                            pts_againstStat = gameInfo['opp_pts']

                            # Season stats
                            team_fgStat = year[team]['teamStats']['fg']['value']
                            team_fgaStat = year[team]['teamStats']['fga']['value']
                            team_fg_pctStat = year[team]['teamStats']['fg_pct']['value']
                            team_fg2Stat = year[team]['teamStats']['fg2']['value']
                            team_fg2aStat = year[team]['teamStats']['fg2a']['value']
                            team_fg2_pctStat = year[team]['teamStats']['fg2_pct']['value']
                            team_fg3Stat = year[team]['teamStats']['fg3']['value']
                            team_fg3aStat = year[team]['teamStats']['fg3a']['value']
                            team_fg3_pctStat = year[team]['teamStats']['fg3_pct']['value']
                            team_ftStat = year[team]['teamStats']['ft']['value']
                            team_ftaStat = year[team]['teamStats']['fta']['value']
                            team_ft_pctStat = year[team]['teamStats']['ft_pct']['value']
                            team_astStat = year[team]['teamStats']['ast']['value']
                            team_ptsStat = year[team]['teamStats']['pts']['value']
                            team_pts_per_gStat = year[team]['teamStats']['pts_per_g']['value']
                            team_orbStat = year[team]['teamStats']['orb']['value']
                            team_drbStat = year[team]['teamStats']['drb']['value']
                            team_trbStat = year[team]['teamStats']['trb']['value']
                            team_stlStat = year[team]['teamStats']['stl']['value']
                            team_blkStat = year[team]['teamStats']['blk']['value']
                            team_tovStat = year[team]['teamStats']['tov']['value']

                            opp_fgStat = year[team]['oppStats']['fg']['value']
                            opp_fgaStat = year[team]['oppStats']['fga']['value']
                            opp_fg_pctStat = year[team]['oppStats']['fg_pct']['value']
                            opp_fg2Stat = year[team]['oppStats']['fg2']['value']
                            opp_fg2aStat = year[team]['oppStats']['fg2a']['value']
                            opp_fg2_pctStat = year[team]['oppStats']['fg2_pct']['value']
                            opp_fg3Stat = year[team]['oppStats']['fg3']['value']
                            opp_fg3aStat = year[team]['oppStats']['fg3a']['value']
                            opp_fg3_pctStat = year[team]['oppStats']['fg3_pct']['value']
                            opp_ftStat = year[team]['oppStats']['ft']['value']
                            opp_ftaStat = year[team]['oppStats']['fta']['value']
                            opp_ft_pctStat = year[team]['oppStats']['ft_pct']['value']
                            opp_astStat = year[team]['oppStats']['ast']['value']
                            opp_ptsStat = year[team]['oppStats']['pts']['value']
                            opp_pts_per_gStat = year[team]['oppStats']['pts_per_g']['value']
                            opp_orbStat = year[team]['oppStats']['orb']['value']
                            opp_drbStat = year[team]['oppStats']['drb']['value']
                            opp_trbStat = year[team]['oppStats']['trb']['value']
                            opp_stlStat = year[team]['oppStats']['stl']['value']
                            opp_blkStat = year[team]['oppStats']['blk']['value']
                            opp_tovStat = year[team]['oppStats']['tov']['value']

                            # Opp Season Stats
                            team2_team_fgStat = year[opponentStat]['teamStats']['fg']['value']
                            team2_team_fgaStat = year[opponentStat]['teamStats']['fga']['value']
                            team2_team_fg_pctStat = year[opponentStat]['teamStats']['fg_pct']['value']
                            team2_team_fg2Stat = year[opponentStat]['teamStats']['fg2']['value']
                            team2_team_fg2aStat = year[opponentStat]['teamStats']['fg2a']['value']
                            team2_team_fg2_pctStat = year[opponentStat]['teamStats']['fg2_pct']['value']
                            team2_team_fg3Stat = year[opponentStat]['teamStats']['fg3']['value']
                            team2_team_fg3aStat = year[opponentStat]['teamStats']['fg3a']['value']
                            team2_team_fg3_pctStat = year[opponentStat]['teamStats']['fg3_pct']['value']
                            team2_team_ftStat = year[opponentStat]['teamStats']['ft']['value']
                            team2_team_ftaStat = year[opponentStat]['teamStats']['fta']['value']
                            team2_team_ft_pctStat = year[opponentStat]['teamStats']['ft_pct']['value']
                            team2_team_astStat = year[opponentStat]['teamStats']['ast']['value']
                            team2_team_ptsStat = year[opponentStat]['teamStats']['pts']['value']
                            team2_team_pts_per_gStat = year[opponentStat]['teamStats']['pts_per_g']['value']
                            team2_team_orbStat = year[opponentStat]['teamStats']['orb']['value']
                            team2_team_drbStat = year[opponentStat]['teamStats']['drb']['value']
                            team2_team_trbStat = year[opponentStat]['teamStats']['trb']['value']
                            team2_team_stlStat = year[opponentStat]['teamStats']['stl']['value']
                            team2_team_blkStat = year[opponentStat]['teamStats']['blk']['value']
                            team2_team_tovStat = year[opponentStat]['teamStats']['tov']['value']

                            team2_opp_fgStat = year[opponentStat]['oppStats']['fg']['value']
                            team2_opp_fgaStat = year[opponentStat]['oppStats']['fga']['value']
                            team2_opp_fg_pctStat = year[opponentStat]['oppStats']['fg_pct']['value']
                            team2_opp_fg2Stat = year[opponentStat]['oppStats']['fg2']['value']
                            team2_opp_fg2aStat = year[opponentStat]['oppStats']['fg2a']['value']
                            team2_opp_fg2_pctStat = year[opponentStat]['oppStats']['fg2_pct']['value']
                            team2_opp_fg3Stat = year[opponentStat]['oppStats']['fg3']['value']
                            team2_opp_fg3aStat = year[opponentStat]['oppStats']['fg3a']['value']
                            team2_opp_fg3_pctStat = year[opponentStat]['oppStats']['fg3_pct']['value']
                            team2_opp_ftStat = year[opponentStat]['oppStats']['ft']['value']
                            team2_opp_ftaStat = year[opponentStat]['oppStats']['fta']['value']
                            team2_opp_ft_pctStat = year[opponentStat]['oppStats']['ft_pct']['value']
                            team2_opp_astStat = year[opponentStat]['oppStats']['ast']['value']
                            team2_opp_ptsStat = year[opponentStat]['oppStats']['pts']['value']
                            team2_opp_pts_per_gStat = year[opponentStat]['oppStats']['pts_per_g']['value']
                            team2_opp_orbStat = year[opponentStat]['oppStats']['orb']['value']
                            team2_opp_drbStat = year[opponentStat]['oppStats']['drb']['value']
                            team2_opp_trbStat = year[opponentStat]['oppStats']['trb']['value']
                            team2_opp_stlStat = year[opponentStat]['oppStats']['stl']['value']
                            team2_opp_blkStat = year[opponentStat]['oppStats']['blk']['value']
                            team2_opp_tovStat = year[opponentStat]['oppStats']['tov']['value']

                            # Insert into list
                            teamName.append(teamNameStat)
                            opponent.append(opponentStat)
                            location.append(locationStat)
                            result.append(resultStat)
                            pts.append(ptsStat)
                            pts_against.append(pts_againstStat)

                            team_fg.append(team_fgStat)
                            team_fga.append(team_fgaStat)
                            team_fg_pct.append(team_fg_pctStat)
                            team_fg2.append(team_fg2Stat)
                            team_fg2a.append(team_fg2aStat)
                            team_fg2_pct.append(team_fg2_pctStat)
                            team_fg3.append(team_fg3Stat)
                            team_fg3a.append(team_fg3aStat)
                            team_fg3_pct.append(team_fg3_pctStat)
                            team_ft.append(team_ftStat)
                            team_fta.append(team_ftaStat)
                            team_ft_pct.append(team_ft_pctStat)
                            team_ast.append(team_astStat)
                            team_pts.append(team_ptsStat)
                            team_pts_per_g.append(team_pts_per_gStat)
                            team_orb.append(team_orbStat)
                            team_drb.append(team_drbStat)
                            team_trb.append(team_trbStat)
                            team_stl.append(team_stlStat)
                            team_blk.append(team_blkStat)
                            team_tov.append(team_tovStat)

                            opp_fg.append(opp_fgStat)
                            opp_fga.append(opp_fgaStat)
                            opp_fg_pct.append(opp_fg_pctStat)
                            opp_fg2.append(opp_fg2Stat)
                            opp_fg2a.append(opp_fg2aStat)
                            opp_fg2_pct.append(opp_fg2_pctStat)
                            opp_fg3.append(opp_fg3Stat)
                            opp_fg3a.append(opp_fg3aStat)
                            opp_fg3_pct.append(opp_fg3_pctStat)
                            opp_ft.append(opp_ftStat)
                            opp_fta.append(opp_ftaStat)
                            opp_ft_pct.append(opp_ft_pctStat)
                            opp_ast.append(opp_astStat)
                            opp_pts.append(opp_ptsStat)
                            opp_pts_per_g.append(opp_pts_per_gStat)
                            opp_orb.append(opp_orbStat)
                            opp_drb.append(opp_drbStat)
                            opp_trb.append(opp_trbStat)
                            opp_stl.append(opp_stlStat)
                            opp_blk.append(opp_blkStat)
                            opp_tov.append(opp_tovStat)

                            team2_team_fg.append(team2_team_fgStat)
                            team2_team_fga.append(team2_team_fgaStat)
                            team2_team_fg_pct.append(team2_team_fg_pctStat)
                            team2_team_fg2.append(team2_team_fg2Stat)
                            team2_team_fg2a.append(team2_team_fg2aStat)
                            team2_team_fg2_pct.append(team2_team_fg2_pctStat)
                            team2_team_fg3.append(team2_team_fg3Stat)
                            team2_team_fg3a.append(team2_team_fg3aStat)
                            team2_team_fg3_pct.append(team2_team_fg3_pctStat)
                            team2_team_ft.append(team2_team_ftStat)
                            team2_team_fta.append(team2_team_ftaStat)
                            team2_team_ft_pct.append(team2_team_ft_pctStat)
                            team2_team_ast.append(team2_team_astStat)
                            team2_team_pts.append(team2_team_ptsStat)
                            team2_team_pts_per_g.append(team2_team_pts_per_gStat)
                            team2_team_orb.append(team2_team_orbStat)
                            team2_team_drb.append(team2_team_drbStat)
                            team2_team_trb.append(team2_team_trbStat)
                            team2_team_stl.append(team2_team_stlStat)
                            team2_team_blk.append(team2_team_blkStat)
                            team2_team_tov.append(team2_team_tovStat)

                            team2_opp_fg.append(team2_opp_fgStat)
                            team2_opp_fga.append(team2_opp_fgaStat)
                            team2_opp_fg_pct.append(team2_opp_fg_pctStat)
                            team2_opp_fg2.append(team2_opp_fg2Stat)
                            team2_opp_fg2a.append(team2_opp_fg2aStat)
                            team2_opp_fg2_pct.append(team2_opp_fg2_pctStat)
                            team2_opp_fg3.append(team2_opp_fg3Stat)
                            team2_opp_fg3a.append(team2_opp_fg3aStat)
                            team2_opp_fg3_pct.append(team2_opp_fg3_pctStat)
                            team2_opp_ft.append(team2_opp_ftStat)
                            team2_opp_fta.append(team2_opp_ftaStat)
                            team2_opp_ft_pct.append(team2_opp_ft_pctStat)
                            team2_opp_ast.append(team2_opp_astStat)
                            team2_opp_pts.append(team2_opp_ptsStat)
                            team2_opp_pts_per_g.append(team2_opp_pts_per_gStat)
                            team2_opp_orb.append(team2_opp_orbStat)
                            team2_opp_drb.append(team2_opp_drbStat)
                            team2_opp_trb.append(team2_opp_trbStat)
                            team2_opp_stl.append(team2_opp_stlStat)
                            team2_opp_blk.append(team2_opp_blkStat)
                            team2_opp_tov.append(team2_opp_tovStat)

                        except KeyError:
                            pass
                except KeyError:
                    pass

data['team'] = teamName
data['opponent'] = opponent
data['location'] = location
data['result'] = result

data['pts'] = pts
data['pts_against'] = pts_against
data['team_fg'] = team_fg
data['team_fga'] = team_fga
data['team_fg_pct'] = team_fg_pct
data['team_fg2'] = team_fg2
data['team_fg2a'] = team_fg2a
data['team_fg2_pct'] = team_fg2_pct
data['team_fg3'] = team_fg3
data['team_fg3a'] = team_fg3a
data['team_fg3_pct'] = team_fg3_pct
data['team_ft'] = team_ft
data['team_fta'] = team_fta
data['team_ft_pct'] = team_ft_pct
data['team_ast'] = team_ast
data['team_pts'] = team_pts
data['team_pts_per_g'] = team_pts_per_g
data['team_orb'] = team_orb
data['team_drb'] = team_drb
data['team_trb'] = team_trb
data['team_stl'] = team_stl
data['team_blk'] = team_blk
data['team_tov'] = team_tov

data['opp_fg'] = opp_fg
data['opp_fga'] = opp_fga
data['opp_fg_pct'] = opp_fg_pct
data['opp_fg2'] = opp_fg2
data['opp_fg2a'] = opp_fg2a
data['opp_fg2_pct'] = opp_fg2_pct
data['opp_fg3'] = opp_fg3
data['opp_fg3a'] = opp_fg3a
data['opp_fg3_pct'] = opp_fg3_pct
data['opp_ft'] = opp_ft
data['opp_fta'] = opp_fta
data['opp_ft_pct'] = opp_ft_pct
data['opp_ast'] = opp_ast
data['opp_pts'] = opp_pts
data['opp_pts_per_g'] = opp_pts_per_g
data['opp_orb'] = opp_orb
data['opp_drb'] = opp_drb
data['opp_trb'] = opp_trb
data['opp_stl'] = opp_stl
data['opp_blk'] = opp_blk
data['opp_tov'] = opp_tov

data['team2_team_fg'] = team2_team_fg
data['team2_team_fga'] = team2_team_fga
data['team2_team_fg_pct'] = team2_team_fg_pct
data['team2_team_fg2'] = team2_team_fg2
data['team2_team_fg2a'] = team2_team_fg2a
data['team2_team_fg2_pct'] = team2_team_fg2_pct
data['team2_team_fg3'] = team2_team_fg3
data['team2_team_fg3a'] = team2_team_fg3a
data['team2_team_fg3_pct'] = team2_team_fg3_pct
data['team2_team_ft'] = team2_team_ft
data['team2_team_fta'] = team2_team_fta
data['team2_team_ft_pct'] = team2_team_ft_pct
data['team2_team_ast'] = team2_team_ast
data['team2_team_pts'] = team2_team_pts
data['team2_team_pts_per_g'] = team2_team_pts_per_g
data['team2_team_orb'] = team2_team_orb
data['team2_team_drb'] = team2_team_drb
data['team2_team_trb'] = team2_team_trb
data['team2_team_stl'] = team2_team_stl
data['team2_team_blk'] = team2_team_blk
data['team2_team_tov'] = team2_team_tov

data['team2_opp_fg'] = team2_opp_fg
data['team2_opp_fga'] = team2_opp_fga
data['team2_opp_fg_pct'] = team2_opp_fg_pct
data['team2_opp_fg2'] = team2_opp_fg2
data['team2_opp_fg2a'] = team2_opp_fg2a
data['team2_opp_fg2_pct'] = team2_opp_fg2_pct
data['team2_opp_fg3'] = team2_opp_fg3
data['team2_opp_fg3a'] = team2_opp_fg3a
data['team2_opp_fg3_pct'] = team2_opp_fg3_pct
data['team2_opp_ft'] = team2_opp_ft
data['team2_opp_fta'] = team2_opp_fta
data['team2_opp_ft_pct'] = team2_opp_ft_pct
data['team2_opp_ast'] = team2_opp_ast
data['team2_opp_pts'] = team2_opp_pts
data['team2_opp_pts_per_g'] = team2_opp_pts_per_g
data['team2_opp_orb'] = team2_opp_orb
data['team2_opp_drb'] = team2_opp_drb
data['team2_opp_trb'] = team2_opp_trb
data['team2_opp_stl'] = team2_opp_stl
data['team2_opp_blk'] = team2_opp_blk
data['team2_opp_tov'] = team2_opp_tov

df = pd.DataFrame(data)
df.to_csv('C:/Users/WVUFa/OneDrive/Documents/CBB/datasets/2018tourney.csv')
