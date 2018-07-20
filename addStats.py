import os
from bs4 import BeautifulSoup
from hashlib import md5
import requests
from pymongo import MongoClient
import re

_CACHE_FOLDER = 'C:/Users/WVUFa/OneDrive/Documents/CBB/cache'
_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

client = MongoClient('localhost', 27017)
db = client['cbb']
col = db.get_collection('stats')
games_col = db.get_collection('games')

if not os.path.exists(_CACHE_FOLDER):
    os.mkdir(_CACHE_FOLDER)


def from_cache(key):
    file_path = os.path.join(_CACHE_FOLDER, key)
    if os.path.exists(file_path):
        return open(file_path).read()


def to_cache(key, data):
    file_path = os.path.join(_CACHE_FOLDER, key)
    open(file_path, 'wb').write(data)


def get_key(text):
    return md5(text.encode()).hexdigest()


def get_web_data(url):
    data = from_cache(get_key(url))
    if data:
        return data
    resp = requests.get(url, headers={'User-Agent': _USER_AGENT})
    if 200 <= resp.status_code < 300:
        to_cache(get_key(url), resp.content)
    return resp.content


# Get team stats
def getTeamStat(teamURL):
    stats = {}
    content = get_web_data(teamURL)
    soup = BeautifulSoup(content, "html.parser")

    teamInfo = soup.find('div', id='meta')

    # Get image
    imgLoc = teamInfo.find('img', class_='teamlogo')
    img = imgLoc['src']
    stats['logo'] = img

    # Get records
    overallStats = teamInfo.find_all('p')
    overallLoc = overallStats[2]
    confLoc = overallStats[3]
    psg = overallStats[5]
    pag = overallStats[6]
    srs = overallStats[7]
    sos = overallStats[8]
    ortg = overallStats[9]
    drtg = overallStats[10]
    overall = re.search('(\d+-\d+)\s(\.\d+)', str(overallLoc))
    conferenceRec = re.search('(\d+-\d+),\s(\d)', str(confLoc))
    pointsScoredGame = re.search('(\d+\.\d+)\s+\((\d+)', str(psg))
    pointsAllowedGame = re.search('(\d+\.\d+)\s+\((\d+)', str(pag))
    simpleRatingSystem = re.search('(-*\d+\.\d+)\s+\((\d+)', str(srs))
    strengthOfSchedule = re.search('(-*\d+\.\d+)\s+\((\d+)', str(sos))
    offensiveRating = re.search('(\d+\.\d+)\s+\((\d+)', str(ortg))
    defensiveRating = re.search('(\d+\.\d+)\s+\((\d+)', str(drtg))

    stats['record'] = overall.group(1)
    stats['winLossPct'] = overall.group(2)
    try:
        stats['conferenceRecord'] = conferenceRec.group(1)
        stats['conferenceRank'] = conferenceRec.group(2)
    except AttributeError:
        stats['conferenceRecord'] = '0-0'
        stats['conferenceRank'] = '0'

    stats['PS/g'] = {'Value': pointsScoredGame.group(1), 'Rank': pointsScoredGame.group(2)}
    stats['PA/g'] = {'Value': pointsAllowedGame.group(1), 'Rank': pointsAllowedGame.group(2)}
    stats['SRS'] = {'Value': simpleRatingSystem.group(1), 'Rank': simpleRatingSystem.group(2)}
    stats['SOS'] = {'Value': strengthOfSchedule.group(1), 'Rank': strengthOfSchedule.group(2)}
    stats['ORtg'] = {'Value': offensiveRating.group(1), 'Rank': offensiveRating.group(2)}
    stats['SOS'] = {'Value': defensiveRating.group(1), 'Rank': defensiveRating.group(2)}

    confName = confLoc.find_all('a')
    stats['conference'] = confName[0].find(text=True)

    # Get team and opponent season stats
    teamStats = {}
    oppStats = {}
    allStats = ['fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a', 'fg3_pct',
                'ft', 'fta', 'ft_pct', 'ast', 'pts', 'pts_per_g', 'orb', 'drb', 'trb', 'stl', 'blk', 'tov']

    table = soup.find('table', class_="suppress_all stats_table", id="team_stats")
    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')

    for dataStat in allStats:
        stat = []
        for row in rows:
            statLoc = row.find_all('td', {'data-stat': dataStat})
            if statLoc:
                stat.append(statLoc[0].find(text=True))
        teamStats[dataStat] = {'value': stat[0], 'rank': stat[1]}

    for dataStat in allStats:
        stat = []
        for row in rows:
            statLoc = row.find_all('td', {'data-stat': 'opp_{}'.format(dataStat)})
            if statLoc:
                stat.append(statLoc[0].find(text=True))
        oppStats[dataStat] = {'value': stat[0], 'rank': stat[1]}

    stats['teamStats'] = teamStats
    stats['oppStats'] = oppStats

    # Get player stats per game
    allPlayerStats = ['g', 'gs', 'mp_per_g', 'fg_per_g', 'fga_per_g', 'fg_pct', 'fg2_per_g', 'fg2a_per_g', 'fg2_pct',
                      'fg3_per_g', 'fg3a_per_g', 'fg3_pct', 'ft_per_g', 'fta_per_g', 'ft_pct',
                      'orb_per_g', 'drb_per_g', 'trb_per_g', 'ast_per_g', 'stl_per_g', 'blk_per_g', 'tov_per_g',
                      'pf_per_g', 'pts_per_g']
    playerTable = soup.find('table', id="per_game")
    playerTableBody = playerTable.find('tbody')
    playerRows = playerTableBody.find_all('tr')

    players = {}
    for row in playerRows:
        aName = row.find_all('a', text=True)
        name = aName[0].find(text=True)
        stat = {}
        for playerStat in allPlayerStats:
            statLoc = row.find_all('td', {'data-stat': playerStat})
            if statLoc:
                stat[playerStat] = statLoc[0].find(text=True)
        players[name] = stat
    stats['players'] = players

    linkDiv = soup.find('div', id='inner_nav')
    links = linkDiv.find_all('li')
    scheduleUrl = links[2].find('a', href=True)['href']
    stats['games'] = getGameResults(scheduleUrl)

    return stats


# Get simple game data for use in team stat db
def getGameResults(url):
    resultsUrl = 'https://www.sports-reference.com{}'.format(url)
    # schedule
    content = get_web_data(resultsUrl)
    soup = BeautifulSoup(content, "html.parser")

    table = soup.find('table', id="schedule")
    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')

    dataStats = ['g', 'date_game', 'game_type', 'opp_name', 'game_result', 'pts', 'opp_pts']
    games = {}
    for row in rows:
        game = {}
        gameDate = row.find_all('td', {'data-stat': 'date_game'})
        try:
            date = gameDate[0].find(text=True)
            for stat in dataStats:
                statLoc = row.find_all('td', {'data-stat': stat})
                if statLoc:
                    game[stat] = statLoc[0].find(text=True)
            games[date] = game
        except TypeError:
            pass
        except AttributeError:
            pass
        except IndexError:
            pass

    return games


# Get detailed gamed data for use in games db
def createGamesDB(teamURL):
    content = get_web_data(teamURL)
    soup = BeautifulSoup(content, "html.parser")

    linkDiv = soup.find('div', id='inner_nav')
    links = linkDiv.find_all('li')
    scheduleUrl = links[2].find('a', href=True)['href']

    resultsUrl = 'https://www.sports-reference.com{}'.format(scheduleUrl)
    # schedule
    content = get_web_data(resultsUrl)
    soup = BeautifulSoup(content, "html.parser")

    table = soup.find('table', id="schedule")
    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')

    dataStats = ['g', 'date_game', 'game_type', 'opp_name', 'game_result', 'pts', 'opp_pts']
    for row in rows:
        game = {}
        game['team'] = name
        gameDate = row.find_all('td', {'data-stat': 'date_game'})
        try:
            date = gameDate[0].find(text=True)
            opp_slice = row.find_all('td', {'data-stat': 'opp_name'})
            try:
                opp_slice_detail = opp_slice[0].find('a', href=True)['href']
            except TypeError:
                opp_slice_detail = opp_slice[0].find(text=True)
            opp_slice_detail = opp_slice_detail.replace('/cbb/schools/', '').replace('/' + year + '.html', '')

            print(date)
            for stat in dataStats:
                statLoc = row.find_all('td', {'data-stat': stat})
                if statLoc:
                    game[stat] = statLoc[0].find(text=True)

            dateLink = gameDate[0].find('a', href=True)['href']
            dateUrl = 'https://www.sports-reference.com{}'.format(dateLink)
            gameContent = get_web_data(dateUrl)
            gameSoup = BeautifulSoup(gameContent, "html.parser")

            basic_team = 'box-score-basic-{}'.format(name.lower().replace('.', '').replace('&', '').replace(' ', '-'))
            basic_opp = 'box-score-basic-{}'.format(
                opp_slice_detail.lower().replace('.', '').replace('&', '').replace(' ', '-').replace('--', '-'))
            advanced_team = 'box-score-advanced-{}'.format(
                name.lower().replace('.', '').replace('&', '').replace(' ', '-'))
            advanced_opp = 'box-score-advanced-{}'.format(
                opp_slice_detail.lower().replace('.', '').replace('&', '').replace(' ', '-').replace('--', '-'))

            print(basic_team)
            print(basic_opp)

            baiscSingleGameStats = ['fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a',
                                    'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast',
                                    'stl', 'blk', 'tov', 'pf']
            advancedSingleGameStats = ['ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct', 'drb_pct',
                                       'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'off_rtg', 'def_rtg']

            basic_team_table = gameSoup.find('table', id=basic_team)
            basic_team_tableBody = basic_team_table.find('tfoot')
            basic_opp_table = gameSoup.find('table', id=basic_opp)
            basic_opp_tableBody = basic_opp_table.find('tfoot')

            for basicStat in baiscSingleGameStats:
                team_statLoc = basic_team_tableBody.find_all('td', {'data-stat': basicStat})
                opp_statLoc = basic_opp_tableBody.find_all('td', {'data-stat': basicStat})
                if team_statLoc:
                    game['team_{}'.format(basicStat)] = team_statLoc[0].find(text=True)
                if opp_statLoc:
                    game['opp_{}'.format(basicStat)] = opp_statLoc[0].find(text=True)
            # TODO: Get advanced stats
            # advanced_team_table = gameSoup.find('table', id=advanced_team)
            # advanced_team_tableBody = advanced_team_table.find('tfoot')
            # advanced_opp_table = gameSoup.find('table', id=advanced_opp)
            # advanced_opp_tableBody = advanced_opp_table.find('tfoot')
            #
            # for advancedStat in advancedSingleGameStats:
            #     team_statLoc = advanced_team_tableBody.find_all('td', {'data-stat': advancedStat})
            #     opp_statLoc = advanced_opp_tableBody.find_all('td', {'data-stat': advancedStat})
            #     if team_statLoc:
            #         game['team_{}'.format(advancedStat)] = team_statLoc[0].find(text=True)
            #     if opp_statLoc:
            #         game['opp_{}'.format(advancedStat)] = opp_statLoc[0].find(text=True)

            games_col.insert(game)
        except AttributeError:
            pass
        except TypeError:
            pass
        except IndexError:
            pass


if __name__ == '__main__':
    # years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    years = ['2018']
    yearIndex = 'https://www.sports-reference.com/cbb/seasons/{}-advanced-school-stats.html'
    for year in years:
        yearUrl = yearIndex.format(year)
        teamIndexPage = get_web_data(yearUrl)
        soup = BeautifulSoup(teamIndexPage, "html.parser")
        table = soup.find('table', id='adv_school_stats')
        tableBody = table.find('tbody')
        rows = tableBody.find_all('tr')
        stats = {}
        for row in rows:
            team = row.find_all('td', {'data-stat': 'school_name'})
            if team:
                name = team[0].find(text=True)

                progress = '{} {}'.format(year, name)
                print(progress)

                urlSlice = team[0].find('a', href=True)['href']
                url = 'https://www.sports-reference.com{}'.format(urlSlice)
                createGamesDB(url)
                teamStats = getTeamStat(url)
                advStats = ['pace', 'off_rtg', 'fta_per_fga_pct', 'fg3a_per_fga_pct', 'ts_pct', 'trb_pct', 'ast_pct',
                            'stl_pct', 'blk_pct', 'efg_pct', 'tov_pct', 'orb_pct', 'ft_rate']
                for advStat in advStats:
                    teamStats[advStat] = row.find_all('td', {'data-stat': advStat})[0].find(text=True)
                stats[name] = teamStats
        col.update({'_id': year}, stats, True)
