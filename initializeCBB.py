import os
import urllib.request
import json
from bs4 import BeautifulSoup
from hashlib import md5
import requests
from pymongo import MongoClient

_TEAMS_URL = 'https://www.sports-reference.com/cbb/schools/'
_OUT_FILE = 'C:/Users/WVUFa/OneDrive/Documents/CBB/teamInfoCopy.json'
_ALIAS_COPY = 'C:/Users/WVUFa/OneDrive/Documents/CBB/teamInfoWithAlias.json'
_CACHE_FOLDER = 'C:/Users/WVUFa/OneDrive/Documents/CBB/cache'
_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

client = MongoClient('localhost', 27017)
db = client['cbb']
col = db.get_collection('headtohead')

# https://www.sports-reference.com/cbb/schools/west-virginia/head-to-head.html HEAD TO HEAD URL EXAMPLE

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


# Initializes JSON file enriched with full team names, and URL for team page
def initializeList():
    allTeams = {}
    teamList = []
    teamUrlList = []

    with urllib.request.urlopen(_TEAMS_URL) as response:
        teamIndexPage = response.read()

    soup = BeautifulSoup(teamIndexPage, "html.parser")
    table = soup.find('table', class_="sortable stats_table")
    rows = table.find_all('tr')
    for row in rows:
        teams = row.find_all('td', {'data-stat': 'school_name'})
        if len(teams) == 1:
            teamList.append(teams[0].find(text=True))
        for a in row.find_all('a', href=True):
            teamUrlList.append(a['href'])

    for i in range(0, len(teamList)):
        allTeams[teamList[i]] = {}
        data = allTeams[teamList[i]]
        data['URL'] = teamUrlList[i]

    json.dump(allTeams, open(_OUT_FILE, 'w'))


# Adds name field (Full name without last word) and two alias fields. Will need to manually fix some fields
def addNames(jsonFile):
    teamInfo = json.load(open(jsonFile, encoding='utf8'))
    allTeams = teamInfo

    for team in teamInfo:
        teamName = team
        shortName = teamName.rsplit(' ', 1)[0]
        allTeams[team]['name'] = shortName.upper()
        allTeams[team]['alias1'] = None
        allTeams[team]['alias2'] = None

    json.dump(allTeams, open(jsonFile, 'w'))


def addHeadToHead(jsonFile):
    teamInfo = json.load(open(jsonFile, encoding='utf8'))
    allTeams = teamInfo

    for team in allTeams:
        allTeams[team]['recordVs'] = {}
        urlSlice = allTeams[team]['URL']
        teamURL = 'https://www.sports-reference.com' + urlSlice + 'head-to-head.html'
        content = get_web_data(teamURL)
        soup = BeautifulSoup(content, "html.parser")
        if soup.find('table', class_="sortable stats_table"):
            table = soup.find('table', class_="sortable stats_table")
            rows = table.find_all('tr')
            for row in rows:
                opponent = row.find_all('td', {'data-stat': 'opp_name'})
                wins = row.find_all('td', {'data-stat': 'wins'})
                losses = row.find_all('td', {'data-stat': 'losses'})
                # history = row.find_all('a', href=True)
                if len(opponent) == 1:
                    # if opponent[0].find(text=True).endswith(';'):
                    #     opponentName = opponent[0].find(text=True)[:-1].upper()
                    if ';' in opponent[0].find(text=True):
                        opponentName = opponent[0].find(text=True).upper().replace(";", "")
                    else:
                        opponentName = opponent[0].find(text=True).upper()
                    allTeams[team]['recordVs'][opponentName] = {}
                    allTeams[team]['recordVs'][opponentName]['Name'] = opponentName
                    allTeams[team]['recordVs'][opponentName]['Wins'] = wins[0].find(text=True)
                    allTeams[team]['recordVs'][opponentName]['Losses'] = losses[0].find(text=True)
                    # getHistoryLink = history[1].get('href')
                    # historyUrl = 'https://www.sports-reference.com' + getHistoryLink
                    # historyContent = get_web_data(historyUrl)
                    # historySoup = BeautifulSoup(historyContent, "html.parser")
                    # if historySoup.find('table', class_='sortable stats_table'):
                    #     historyTable = historySoup.find('table', class_="sortable stats_table")
                    #     historyRows = historyTable.find_all('tr')
                    #     for historyRow in historyRows:
                    #         season = historyRow.find_all('td', {'data-stat': 'year_id'})
                    #         date = historyRow.find_all('td', {'data-stat': 'date_game'})
                    #         result = historyRow.find_all('td', {'data-stat': 'game_result'})
                    #         pts = historyRow.find_all('td', {'data-stat': 'pts'})
                    #         oppPts = historyRow.find_all('td', {'data-stat': 'opp_pts'})
                    #         if len(season) == 1:
                    #             allTeams[team]['recordVs'][opponentName]['history'] = {}
                    #             allTeams[team]['recordVs'][opponentName]['history']['season'] = season[0].find(text=True)
                    #             allTeams[team]['recordVs'][opponentName]['history']['season'] = date[0].find(text=True)
                    #             allTeams[team]['recordVs'][opponentName]['history']['season'] = result[0].find(text=True)
                    #             allTeams[team]['recordVs'][opponentName]['history']['season'] = pts[0].find(text=True)
                    #             allTeams[team]['recordVs'][opponentName]['history']['season'] = oppPts[0].find(text=True)

    json.dump(allTeams, open(jsonFile, 'w'))


def seeTeamNames(jsonFile):
    teamNames = []
    teamInfo = json.load(open(jsonFile, encoding='utf8'))
    allTeams = teamInfo
    for team in allTeams:
        if allTeams[team]['recordVs']:
            for opponent in allTeams[team]['recordVs']:
                opponentName = allTeams[team]['recordVs'][opponent]['Name']
                if opponentName not in teamNames:
                    teamNames.append(opponentName)
    sortedTeams = sorted(teamNames)
    for teams in sortedTeams:
        print(teams)

def insertIntoDB(jsonFile):
    data = json.load(open(jsonFile, encoding='utf8'))
    for d in data:
        print(data[d])
        #col.update({'_id': data[d]['name']}, data[d], True)


if __name__ == '__main__':
    #initializeList()
    #addNames(_OUT_FILE)
    #addHeadToHead(_ALIAS_COPY)
    #seeTeamNames(_OUT_FILE)
    insertIntoDB(_ALIAS_COPY)
    print("Head to Head successfully initialized")
