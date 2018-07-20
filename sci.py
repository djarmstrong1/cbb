from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import linear_model
from sklearn import svm
from sklearn import tree
from sklearn.linear_model import SGDClassifier
import numpy as np
import pandas as pd
from pymongo import MongoClient

# TODO: Use regression testing to compute game stats
client = MongoClient('localhost', 27017)
db = client['cbb']
collection = db.get_collection('stats').find({'_id': '2018'})

df = pd.read_csv('C:/Users/WVUFa/OneDrive/Documents/CBB/datasets/allGamesV2.csv')
tourney_df = pd.read_csv('C:/Users/WVUFa/OneDrive/Documents/CBB/datasets/tourneyGamesV2.csv')
tourney2018_df = pd.read_csv('C:/Users/WVUFa/OneDrive/Documents/CBB/datasets/2018tourney.csv')

X = np.array(
    [df['team_fg'], df['team_fga'], df['team_fg_pct'], df['team_fg2'],
     df['team_fg2a'], df['team_fg2_pct'], df['team_fg3'], df['team_fg3a'], df['team_fg3_pct'], df['team_ft'],
     df['team_fta'], df['team_ft_pct'], df['team_ast'], df['team_pts'], df['team_pts_per_g'], df['team_orb'],
     df['team_drb'], df['team_trb'], df['team_stl'], df['team_blk'], df['team_tov'], df['opp_fg'], df['opp_fga'],
     df['opp_fg_pct'], df['opp_fg2'], df['opp_fg2a'], df['opp_fg2_pct'], df['opp_fg3'], df['opp_fg3a'],
     df['opp_fg3_pct'], df['opp_ft'], df['opp_fta'], df['opp_ft_pct'], df['opp_ast'], df['opp_pts'],
     df['opp_pts_per_g'], df['opp_orb'], df['opp_drb'], df['opp_trb'], df['opp_stl'], df['opp_blk'], df['opp_tov'],
     df['team2_team_fg'], df['team2_team_fga'], df['team2_team_fg_pct'], df['team2_team_fg2'], df['team2_team_fg2a'],
     df['team2_team_fg2_pct'], df['team2_team_fg3'], df['team2_team_fg3a'], df['team2_team_fg3_pct'],
     df['team2_team_ft'], df['team2_team_fta'], df['team2_team_ft_pct'], df['team2_team_ast'], df['team2_team_pts'],
     df['team2_team_pts_per_g'], df['team2_team_orb'], df['team2_team_drb'], df['team2_team_trb'], df['team2_team_stl'],
     df['team2_team_blk'], df['team2_team_tov'], df['team2_opp_fg'], df['team2_opp_fga'], df['team2_opp_fg_pct'],
     df['team2_opp_fg2'], df['team2_opp_fg2a'], df['team2_opp_fg2_pct'], df['team2_opp_fg3'], df['team2_opp_fg3a'],
     df['team2_opp_fg3_pct'], df['team2_opp_ft'], df['team2_opp_fta'], df['team2_opp_ft_pct'], df['team2_opp_ast'],
     df['team2_opp_pts'], df['team2_opp_pts_per_g'], df['team2_opp_orb'], df['team2_opp_drb'], df['team2_opp_trb'],
     df['team2_opp_stl'], df['team2_opp_blk'], df['team2_opp_tov']
     ])
y = np.array(df['result'])
X_Test = np.array(
    [tourney_df['team_fg'], tourney_df['team_fga'], tourney_df['team_fg_pct'], tourney_df['team_fg2'],
     tourney_df['team_fg2a'], tourney_df['team_fg2_pct'], tourney_df['team_fg3'], tourney_df['team_fg3a'],
     tourney_df['team_fg3_pct'], tourney_df['team_ft'],
     tourney_df['team_fta'], tourney_df['team_ft_pct'], tourney_df['team_ast'], tourney_df['team_pts'],
     tourney_df['team_pts_per_g'], tourney_df['team_orb'],
     tourney_df['team_drb'], tourney_df['team_trb'], tourney_df['team_stl'], tourney_df['team_blk'],
     tourney_df['team_tov'], tourney_df['opp_fg'], tourney_df['opp_fga'],
     tourney_df['opp_fg_pct'], tourney_df['opp_fg2'], tourney_df['opp_fg2a'], tourney_df['opp_fg2_pct'],
     tourney_df['opp_fg3'], tourney_df['opp_fg3a'],
     tourney_df['opp_fg3_pct'], tourney_df['opp_ft'], tourney_df['opp_fta'], tourney_df['opp_ft_pct'],
     tourney_df['opp_ast'], tourney_df['opp_pts'],
     tourney_df['opp_pts_per_g'], tourney_df['opp_orb'], tourney_df['opp_drb'], tourney_df['opp_trb'],
     tourney_df['opp_stl'], tourney_df['opp_blk'], tourney_df['opp_tov'],
     tourney_df['team2_team_fg'], tourney_df['team2_team_fga'], tourney_df['team2_team_fg_pct'],
     tourney_df['team2_team_fg2'], tourney_df['team2_team_fg2a'],
     tourney_df['team2_team_fg2_pct'], tourney_df['team2_team_fg3'], tourney_df['team2_team_fg3a'],
     tourney_df['team2_team_fg3_pct'],
     tourney_df['team2_team_ft'], tourney_df['team2_team_fta'], tourney_df['team2_team_ft_pct'],
     tourney_df['team2_team_ast'], tourney_df['team2_team_pts'],
     tourney_df['team2_team_pts_per_g'], tourney_df['team2_team_orb'], tourney_df['team2_team_drb'],
     tourney_df['team2_team_trb'], tourney_df['team2_team_stl'],
     tourney_df['team2_team_blk'], tourney_df['team2_team_tov'], tourney_df['team2_opp_fg'],
     tourney_df['team2_opp_fga'], tourney_df['team2_opp_fg_pct'],
     tourney_df['team2_opp_fg2'], tourney_df['team2_opp_fg2a'], tourney_df['team2_opp_fg2_pct'],
     tourney_df['team2_opp_fg3'], tourney_df['team2_opp_fg3a'],
     tourney_df['team2_opp_fg3_pct'], tourney_df['team2_opp_ft'], tourney_df['team2_opp_fta'],
     tourney_df['team2_opp_ft_pct'], tourney_df['team2_opp_ast'],
     tourney_df['team2_opp_pts'], tourney_df['team2_opp_pts_per_g'], tourney_df['team2_opp_orb'],
     tourney_df['team2_opp_drb'], tourney_df['team2_opp_trb'],
     tourney_df['team2_opp_stl'], tourney_df['team2_opp_blk'], tourney_df['team2_opp_tov']
     ])
y_Test = np.array(tourney_df['result'])

X = X.transpose()
X_Test = X_Test.transpose()


def getSingleMatchup(teamA, teamB):
    data = {}
    data['team_fg'] = collection[0][teamA]['teamStats']['fg']['value']
    data['team_fga'] = collection[0][teamA]['teamStats']['fga']['value']
    data['team_fg_pct'] = collection[0][teamA]['teamStats']['fg_pct']['value']
    data['team_fg2'] = collection[0][teamA]['teamStats']['fg2']['value']
    data['team_fg2a'] = collection[0][teamA]['teamStats']['fg2a']['value']
    data['team_fg2_pct'] = collection[0][teamA]['teamStats']['fg2_pct']['value']
    data['team_fg3'] = collection[0][teamA]['teamStats']['fg3']['value']
    data['team_fg3a'] = collection[0][teamA]['teamStats']['fg3a']['value']
    data['team_fg3_pct'] = collection[0][teamA]['teamStats']['fg3_pct']['value']
    data['team_ft'] = collection[0][teamA]['teamStats']['ft']['value']
    data['team_fta'] = collection[0][teamA]['teamStats']['fta']['value']
    data['team_ft_pct'] = collection[0][teamA]['teamStats']['ft_pct']['value']
    data['team_ast'] = collection[0][teamA]['teamStats']['ast']['value']
    data['team_pts'] = collection[0][teamA]['teamStats']['pts']['value']
    data['team_pts_per_g'] = collection[0][teamA]['teamStats']['pts_per_g']['value']
    data['team_orb'] = collection[0][teamA]['teamStats']['orb']['value']
    data['team_drb'] = collection[0][teamA]['teamStats']['drb']['value']
    data['team_trb'] = collection[0][teamA]['teamStats']['trb']['value']
    data['team_stl'] = collection[0][teamA]['teamStats']['stl']['value']
    data['team_blk'] = collection[0][teamA]['teamStats']['blk']['value']
    data['team_tov'] = collection[0][teamA]['teamStats']['tov']['value']

    data['opp_fg'] = collection[0][teamA]['oppStats']['fg']['value']
    data['opp_fga'] = collection[0][teamA]['oppStats']['fga']['value']
    data['opp_fg_pct'] = collection[0][teamA]['oppStats']['fg_pct']['value']
    data['opp_fg2'] = collection[0][teamA]['oppStats']['fg2']['value']
    data['opp_fg2a'] = collection[0][teamA]['oppStats']['fg2a']['value']
    data['opp_fg2_pct'] = collection[0][teamA]['oppStats']['fg2_pct']['value']
    data['opp_fg3'] = collection[0][teamA]['oppStats']['fg3']['value']
    data['opp_fg3a'] = collection[0][teamA]['oppStats']['fg3a']['value']
    data['opp_fg3_pct'] = collection[0][teamA]['oppStats']['fg3_pct']['value']
    data['opp_ft'] = collection[0][teamA]['oppStats']['ft']['value']
    data['opp_fta'] = collection[0][teamA]['oppStats']['fta']['value']
    data['opp_ft_pct'] = collection[0][teamA]['oppStats']['ft_pct']['value']
    data['opp_ast'] = collection[0][teamA]['oppStats']['ast']['value']
    data['opp_pts'] = collection[0][teamA]['oppStats']['pts']['value']
    data['opp_pts_per_g'] = collection[0][teamA]['oppStats']['pts_per_g']['value']
    data['opp_orb'] = collection[0][teamA]['oppStats']['orb']['value']
    data['opp_drb'] = collection[0][teamA]['oppStats']['drb']['value']
    data['opp_trb'] = collection[0][teamA]['oppStats']['trb']['value']
    data['opp_stl'] = collection[0][teamA]['oppStats']['stl']['value']
    data['opp_blk'] = collection[0][teamA]['oppStats']['blk']['value']
    data['opp_tov'] = collection[0][teamA]['oppStats']['tov']['value']

    data['team2_team_fg'] = collection[0][teamB]['teamStats']['fg']['value']
    data['team2_team_fga'] = collection[0][teamB]['teamStats']['fga']['value']
    data['team2_team_fg_pct'] = collection[0][teamB]['teamStats']['fg_pct']['value']
    data['team2_team_fg2'] = collection[0][teamB]['teamStats']['fg2']['value']
    data['team2_team_fg2a'] = collection[0][teamB]['teamStats']['fg2a']['value']
    data['team2_team_fg2_pct'] = collection[0][teamB]['teamStats']['fg2_pct']['value']
    data['team2_team_fg3'] = collection[0][teamB]['teamStats']['fg3']['value']
    data['team2_team_fg3a'] = collection[0][teamB]['teamStats']['fg3a']['value']
    data['team2_team_fg3_pct'] = collection[0][teamB]['teamStats']['fg3_pct']['value']
    data['team2_team_ft'] = collection[0][teamB]['teamStats']['ft']['value']
    data['team2_team_fta'] = collection[0][teamB]['teamStats']['fta']['value']
    data['team2_team_ft_pct'] = collection[0][teamB]['teamStats']['ft_pct']['value']
    data['team2_team_ast'] = collection[0][teamB]['teamStats']['ast']['value']
    data['team2_team_pts'] = collection[0][teamB]['teamStats']['pts']['value']
    data['team2_team_pts_per_g'] = collection[0][teamB]['teamStats']['pts_per_g']['value']
    data['team2_team_orb'] = collection[0][teamB]['teamStats']['orb']['value']
    data['team2_team_drb'] = collection[0][teamB]['teamStats']['drb']['value']
    data['team2_team_trb'] = collection[0][teamB]['teamStats']['trb']['value']
    data['team2_team_stl'] = collection[0][teamB]['teamStats']['stl']['value']
    data['team2_team_blk'] = collection[0][teamB]['teamStats']['blk']['value']
    data['team2_team_tov'] = collection[0][teamB]['teamStats']['tov']['value']

    data['team2_opp_fg'] = collection[0][teamB]['oppStats']['fg']['value']
    data['team2_opp_fga'] = collection[0][teamB]['oppStats']['fga']['value']
    data['team2_opp_fg_pct'] = collection[0][teamB]['oppStats']['fg_pct']['value']
    data['team2_opp_fg2'] = collection[0][teamB]['oppStats']['fg2']['value']
    data['team2_opp_fg2a'] = collection[0][teamB]['oppStats']['fg2a']['value']
    data['team2_opp_fg2_pct'] = collection[0][teamB]['oppStats']['fg2_pct']['value']
    data['team2_opp_fg3'] = collection[0][teamB]['oppStats']['fg3']['value']
    data['team2_opp_fg3a'] = collection[0][teamB]['oppStats']['fg3a']['value']
    data['team2_opp_fg3_pct'] = collection[0][teamB]['oppStats']['fg3_pct']['value']
    data['team2_opp_ft'] = collection[0][teamB]['oppStats']['ft']['value']
    data['team2_opp_fta'] = collection[0][teamB]['oppStats']['fta']['value']
    data['team2_opp_ft_pct'] = collection[0][teamB]['oppStats']['ft_pct']['value']
    data['team2_opp_ast'] = collection[0][teamB]['oppStats']['ast']['value']
    data['team2_opp_pts'] = collection[0][teamB]['oppStats']['pts']['value']
    data['team2_opp_pts_per_g'] = collection[0][teamB]['oppStats']['pts_per_g']['value']
    data['team2_opp_orb'] = collection[0][teamB]['oppStats']['orb']['value']
    data['team2_opp_drb'] = collection[0][teamB]['oppStats']['drb']['value']
    data['team2_opp_trb'] = collection[0][teamB]['oppStats']['trb']['value']
    data['team2_opp_stl'] = collection[0][teamB]['oppStats']['stl']['value']
    data['team2_opp_blk'] = collection[0][teamB]['oppStats']['blk']['value']
    data['team2_opp_tov'] = collection[0][teamB]['oppStats']['tov']['value']

    li = list(data.values())
    toNp = np.array(li)
    toNp = toNp.reshape(-1, 1)
    toNp = toNp.transpose()
    return toNp.astype(np.float)


def predictWinner(teamA, teamB):
    matchupData = getSingleMatchup(teamA, teamB)
    prediction = LogisticPredictions(matchupData)
    if prediction[0] == 'W':
        winner = teamA
    else:
        winner = teamB
    return winner


def pctTest(teamA, teamB, n):
    matchupData = getSingleMatchup(teamA, teamB)
    teamAcount = 0
    teamBcount = 0
    for i in range(0, n):
        prediction = SDGCPrediction(matchupData)
        if prediction[0] == 'W':
            teamAcount += 1
        else:
            teamBcount += 1
    toPrint = '{} wins {}% of the time'.format(teamA, teamAcount / n * 100)
    print(toPrint)


def testDataset(prediction):
    count = 0
    for i in range(0, len(y_Test)):
        if prediction[i] == y_Test[i]:
            count += 1
    pct = count / len(y_Test) * 100
    toPrint = 'Predicted {}% of results successfully'.format(pct)
    print(toPrint)


def testTourneySet(prediction, confidence):
    count = 0
    y_2018 = np.array(tourney2018_df['result'])
    for i in range(0, len(y_2018)):
        print('{} vs {} - Actual: {} Predicted: {} Confidence: {}'.format(tourney2018_df.loc[i]['team'], tourney2018_df.loc[i]['opponent'],
                                                                          y_2018[i], prediction[i], confidence[i]))
        if prediction[i] == y_2018[i]:
            count += 1
    pct = count / len(y_2018) * 100
    toPrint = 'Predicted {}% of results successfully'.format(pct)
    print(toPrint)


# 70% Success
def KNeighborClassifierPredictions(X_predict):
    knn = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
                               metric_params=None, n_jobs=1, n_neighbors=5, p=2,
                               weights='uniform')
    knn.fit(X, y)
    return knn.predict(X_predict)


# 72.83% Success
# Slightly better on larger dataset
def NearestCentroidPredictions(X_predict):
    clf = NearestCentroid(metric='euclidean', shrink_threshold=None)
    clf.fit(X, y)
    return clf.predict(X_predict)


# 73.41% Success
def LogisticPredictions(X_predict):
    logistic = linear_model.LogisticRegression(C=100000.0, class_weight=None, dual=False,
                                               fit_intercept=True, intercept_scaling=1, max_iter=100,
                                               multi_class='ovr', n_jobs=1, penalty='l2', random_state=None,
                                               solver='liblinear', tol=0.0001, verbose=0, warm_start=False)
    logistic.fit(X, y)
    return logistic.predict(X_predict)


# 54.62 - 74% Success
def LinearSVCPrediction(X_predict):
    clf = svm.LinearSVC(penalty='l2', loss='squared_hinge', dual=True, tol=0.0001, C=1.0, multi_class='ovr',
                        fit_intercept=True, intercept_scaling=1, class_weight=None, verbose=0, random_state=None,
                        max_iter=1000)
    clf.fit(X, y)
    return clf.predict(X_predict)


# 55-60% Success
def treePrediction(X_predict):
    clf = tree.DecisionTreeClassifier()
    clf.fit(X, y)
    # Could adapt predict_proba
    return clf.predict(X_predict)


# 50 - 70% Success
def SDGCPrediction(X_predict):
    clf = SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
                        eta0=0.0, fit_intercept=True, l1_ratio=0.15,
                        learning_rate='optimal', loss='hinge', max_iter=None, n_iter=None,
                        n_jobs=1, penalty='l2', power_t=0.5, random_state=None,
                        shuffle=True, tol=None, verbose=0, warm_start=False)
    clf.fit(X, y)
    # Could adapt predict proba
    return clf.predict(X_predict)

# Logistic seems to be best model for total season stats prediction
# TODO: Use datasets on single game stats data
# TODO: First try classification to get result, then try regression to predict pts and statline
if __name__ == '__main__':
    # testDataset(LogisticPredictions(X_Test))
    # testTourneySet(SDGCPrediction(X_Test))
    print(predictWinner('West Virginia', 'Virginia'))
    # pctTest('Oklahoma', 'Rhode Island', 100)


    # Test for pct of SGDC
    # predictions = []
    # confidence = []
    # for index, row in tourney2018_df.iterrows():
    #     oneGame = np.array(
    #         [row['team_fg'], row['team_fga'], row['team_fg_pct'], row['team_fg2'],
    #          row['team_fg2a'], row['team_fg2_pct'], row['team_fg3'], row['team_fg3a'],
    #          row['team_fg3_pct'], row['team_ft'],
    #          row['team_fta'], row['team_ft_pct'], row['team_ast'], row['team_pts'],
    #          row['team_pts_per_g'], row['team_orb'],
    #          row['team_drb'], row['team_trb'], row['team_stl'], row['team_blk'],
    #          row['team_tov'], row['opp_fg'], row['opp_fga'],
    #          row['opp_fg_pct'], row['opp_fg2'], row['opp_fg2a'], row['opp_fg2_pct'],
    #          row['opp_fg3'], row['opp_fg3a'],
    #          row['opp_fg3_pct'], row['opp_ft'], row['opp_fta'], row['opp_ft_pct'],
    #          row['opp_ast'], row['opp_pts'],
    #          row['opp_pts_per_g'], row['opp_orb'], row['opp_drb'], row['opp_trb'],
    #          row['opp_stl'], row['opp_blk'], row['opp_tov'],
    #          row['team2_team_fg'], row['team2_team_fga'], row['team2_team_fg_pct'],
    #          row['team2_team_fg2'], row['team2_team_fg2a'],
    #          row['team2_team_fg2_pct'], row['team2_team_fg3'], row['team2_team_fg3a'],
    #          row['team2_team_fg3_pct'],
    #          row['team2_team_ft'], row['team2_team_fta'], row['team2_team_ft_pct'],
    #          row['team2_team_ast'], row['team2_team_pts'],
    #          row['team2_team_pts_per_g'], row['team2_team_orb'], row['team2_team_drb'],
    #          row['team2_team_trb'], row['team2_team_stl'],
    #          row['team2_team_blk'], row['team2_team_tov'], row['team2_opp_fg'],
    #          row['team2_opp_fga'], row['team2_opp_fg_pct'],
    #          row['team2_opp_fg2'], row['team2_opp_fg2a'], row['team2_opp_fg2_pct'],
    #          row['team2_opp_fg3'], row['team2_opp_fg3a'],
    #          row['team2_opp_fg3_pct'], row['team2_opp_ft'], row['team2_opp_fta'],
    #          row['team2_opp_ft_pct'], row['team2_opp_ast'],
    #          row['team2_opp_pts'], row['team2_opp_pts_per_g'], row['team2_opp_orb'],
    #          row['team2_opp_drb'], row['team2_opp_trb'],
    #          row['team2_opp_stl'], row['team2_opp_blk'], row['team2_opp_tov']
    #          ])
    #     oneGame = oneGame.reshape(-1, 1)
    #     oneGame = oneGame.transpose()
    #     oneGame = oneGame.astype(np.float)
    #     teamAcount = 0
    #     for i in range(0, 101):
    #         prediction = SDGCPrediction(oneGame)
    #         if prediction[0] == 'W':
    #             teamAcount += 1
    #     if teamAcount > 50:
    #         predictions.append('W')
    #         confidence.append(teamAcount / 101 * 100)
    #     else:
    #         predictions.append('L')
    #         confidence.append((100 - teamAcount) / 101 * 100)
    # testTourneySet(predictions, confidence)


    # Test for each data model
    # allModels = [KNeighborClassifierPredictions(X_Test), NearestCentroidPredictions(X_Test),
    #              LogisticPredictions(X_Test), LinearSVCPrediction(X_Test), treePrediction(X_Test),
    #              SDGCPrediction(X_Test)]
    # allModelsNames = ['KNeighborClassifierPredictions', 'NearestCentroidPredictions',
    #              'LogisticPredictions', 'LinearSVCPrediction', 'treePrediction',
    #              'SDGCPrediction']
    # index = 0
    # for model in allModels:
    #     toPrint = '{}: {}'.format(allModelsNames[index], testDataset(model))
    #     index += 1
    #     print(toPrint)
