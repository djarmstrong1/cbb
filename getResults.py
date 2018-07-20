from pymongo import MongoClient
import re

client = MongoClient('localhost', 27017)
db = client['cbb']


def findTeamName(inputName):
    if db.get_collection('headtohead').find({'name': inputName}).count() > 0:
        return inputName
    elif db.get_collection('headtohead').find({'alias1': inputName}).count() > 0:
        col = db.get_collection('headtohead').find({'alias1': inputName})
        return col[0]['name']
    elif db.get_collection('headtohead').find({'alias2': inputName}).count() > 0:
        col = db.get_collection('headtohead').find({'alias2': inputName})
        return col[0]['name']
    else:
        return None


def getHeadtoHead(teamA, teamB):
    if isinstance(teamA, str) and isinstance(teamB, str):
        teamOne = teamA.upper()
        teamTwo = teamB.upper()
        if findTeamName(teamOne) and findTeamName(teamTwo):
            teamOneName = findTeamName(teamOne)
            teamTwoName = findTeamName(teamTwo)
            search = 'recordVs.'+teamTwoName
            if db.get_collection('headtohead').find({'name': teamOneName, search: {'$exists': True}}).count() > 0:
                teamOneResults = db.get_collection('headtohead').find({'name': teamOneName})
                wins = teamOneResults[0]['recordVs'][teamTwoName]['Wins']
                losses = teamOneResults[0]['recordVs'][teamTwoName]['Losses']
                output = 'Series Record: ' + teamOneName + " " + wins + " - " + losses + " " + teamTwoName
            else:
                output = 'These two teams have never met'
            return output
    return None


if __name__ == '__main__':
    userInput = "Test"
    print("Enter a game result in following format: Team A vs Team B")
    print("Example: West Virginia vs Pittsburgh\n")
    while userInput != "":
        userInput = input()
        try:
            inputString = re.search('([\w+\s*]+)+\s*(vs)\s*([\w+\s*]+)+', userInput)
            teamA = inputString[1].rstrip(" ")
            teamB = inputString[3].lstrip(" ")
            if getHeadtoHead(teamA=teamA, teamB=teamB):
                print(getHeadtoHead(teamA=teamA, teamB=teamB))
            print("")
        except Exception:
            print("")
            pass
    print("Exited Program")
