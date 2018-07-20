import re
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['cbb']
collection = db.get_collection('stats')

teamOptions = [{'label': 'Abilene Christian', 'value': 'Abilene Christian'},
               {'label': 'Air Force', 'value': 'Air Force'}, {'label': 'Akron', 'value': 'Akron'},
               {'label': 'Alabama A&M', 'value': 'Alabama A&M'},
               {'label': 'Alabama-Birmingham', 'value': 'Alabama-Birmingham'},
               {'label': 'Alabama State', 'value': 'Alabama State'}, {'label': 'Alabama', 'value': 'Alabama'},
               {'label': 'Albany (NY)', 'value': 'Albany (NY)'}, {'label': 'Alcorn State', 'value': 'Alcorn State'},
               {'label': 'American', 'value': 'American'}, {'label': 'Appalachian State', 'value': 'Appalachian State'},
               {'label': 'Arizona State', 'value': 'Arizona State'}, {'label': 'Arizona', 'value': 'Arizona'},
               {'label': 'Little Rock', 'value': 'Little Rock'},
               {'label': 'Arkansas-Pine Bluff', 'value': 'Arkansas-Pine Bluff'},
               {'label': 'Arkansas State', 'value': 'Arkansas State'}, {'label': 'Arkansas', 'value': 'Arkansas'},
               {'label': 'Army', 'value': 'Army'}, {'label': 'Auburn', 'value': 'Auburn'},
               {'label': 'Austin Peay', 'value': 'Austin Peay'}, {'label': 'Ball State', 'value': 'Ball State'},
               {'label': 'Baylor', 'value': 'Baylor'}, {'label': 'Belmont', 'value': 'Belmont'},
               {'label': 'Bethune-Cookman', 'value': 'Bethune-Cookman'}, {'label': 'Binghamton', 'value': 'Binghamton'},
               {'label': 'Boise State', 'value': 'Boise State'}, {'label': 'Boston College', 'value': 'Boston College'},
               {'label': 'Boston University', 'value': 'Boston University'},
               {'label': 'Bowling Green State', 'value': 'Bowling Green State'},
               {'label': 'Bradley', 'value': 'Bradley'}, {'label': 'Brigham Young', 'value': 'Brigham Young'},
               {'label': 'Brown', 'value': 'Brown'}, {'label': 'Bryant', 'value': 'Bryant'},
               {'label': 'Bucknell', 'value': 'Bucknell'}, {'label': 'Buffalo', 'value': 'Buffalo'},
               {'label': 'Butler', 'value': 'Butler'}, {'label': 'Cal Poly', 'value': 'Cal Poly'},
               {'label': 'Cal State Bakersfield', 'value': 'Cal State Bakersfield'},
               {'label': 'Cal State Fullerton', 'value': 'Cal State Fullerton'},
               {'label': 'Cal State Northridge', 'value': 'Cal State Northridge'},
               {'label': 'UC-Davis', 'value': 'UC-Davis'}, {'label': 'UC-Irvine', 'value': 'UC-Irvine'},
               {'label': 'UC-Riverside', 'value': 'UC-Riverside'},
               {'label': 'UC-Santa Barbara', 'value': 'UC-Santa Barbara'},
               {'label': 'University of California', 'value': 'University of California'},
               {'label': 'Campbell', 'value': 'Campbell'}, {'label': 'Canisius', 'value': 'Canisius'},
               {'label': 'Central Arkansas', 'value': 'Central Arkansas'},
               {'label': 'Central Connecticut State', 'value': 'Central Connecticut State'},
               {'label': 'Central Florida', 'value': 'Central Florida'},
               {'label': 'Central Michigan', 'value': 'Central Michigan'},
               {'label': 'Charleston Southern', 'value': 'Charleston Southern'},
               {'label': 'Charlotte', 'value': 'Charlotte'}, {'label': 'Chattanooga', 'value': 'Chattanooga'},
               {'label': 'Chicago State', 'value': 'Chicago State'}, {'label': 'Cincinnati', 'value': 'Cincinnati'},
               {'label': 'Citadel', 'value': 'Citadel'}, {'label': 'Clemson', 'value': 'Clemson'},
               {'label': 'Cleveland State', 'value': 'Cleveland State'},
               {'label': 'Coastal Carolina', 'value': 'Coastal Carolina'}, {'label': 'Colgate', 'value': 'Colgate'},
               {'label': 'College of Charleston', 'value': 'College of Charleston'},
               {'label': 'Colorado State', 'value': 'Colorado State'}, {'label': 'Colorado', 'value': 'Colorado'},
               {'label': 'Columbia', 'value': 'Columbia'}, {'label': 'Connecticut', 'value': 'Connecticut'},
               {'label': 'Coppin State', 'value': 'Coppin State'}, {'label': 'Cornell', 'value': 'Cornell'},
               {'label': 'Creighton', 'value': 'Creighton'}, {'label': 'Dartmouth', 'value': 'Dartmouth'},
               {'label': 'Davidson', 'value': 'Davidson'}, {'label': 'Dayton', 'value': 'Dayton'},
               {'label': 'Delaware State', 'value': 'Delaware State'}, {'label': 'Delaware', 'value': 'Delaware'},
               {'label': 'Denver', 'value': 'Denver'}, {'label': 'DePaul', 'value': 'DePaul'},
               {'label': 'Detroit Mercy', 'value': 'Detroit Mercy'}, {'label': 'Drake', 'value': 'Drake'},
               {'label': 'Drexel', 'value': 'Drexel'}, {'label': 'Duke', 'value': 'Duke'},
               {'label': 'Duquesne', 'value': 'Duquesne'}, {'label': 'East Carolina', 'value': 'East Carolina'},
               {'label': 'East Tennessee State', 'value': 'East Tennessee State'},
               {'label': 'Eastern Illinois', 'value': 'Eastern Illinois'},
               {'label': 'Eastern Kentucky', 'value': 'Eastern Kentucky'},
               {'label': 'Eastern Michigan', 'value': 'Eastern Michigan'},
               {'label': 'Eastern Washington', 'value': 'Eastern Washington'}, {'label': 'Elon', 'value': 'Elon'},
               {'label': 'Evansville', 'value': 'Evansville'}, {'label': 'Fairfield', 'value': 'Fairfield'},
               {'label': 'Fairleigh Dickinson', 'value': 'Fairleigh Dickinson'},
               {'label': 'Florida A&M', 'value': 'Florida A&M'},
               {'label': 'Florida Atlantic', 'value': 'Florida Atlantic'},
               {'label': 'Florida Gulf Coast', 'value': 'Florida Gulf Coast'},
               {'label': 'Florida International', 'value': 'Florida International'},
               {'label': 'Florida State', 'value': 'Florida State'}, {'label': 'Florida', 'value': 'Florida'},
               {'label': 'Fordham', 'value': 'Fordham'}, {'label': 'Fresno State', 'value': 'Fresno State'},
               {'label': 'Furman', 'value': 'Furman'}, {'label': 'Gardner-Webb', 'value': 'Gardner-Webb'},
               {'label': 'George Mason', 'value': 'George Mason'},
               {'label': 'George Washington', 'value': 'George Washington'},
               {'label': 'Georgetown', 'value': 'Georgetown'},
               {'label': 'Georgia Southern', 'value': 'Georgia Southern'},
               {'label': 'Georgia State', 'value': 'Georgia State'}, {'label': 'Georgia Tech', 'value': 'Georgia Tech'},
               {'label': 'Georgia', 'value': 'Georgia'}, {'label': 'Gonzaga', 'value': 'Gonzaga'},
               {'label': 'Grambling', 'value': 'Grambling'}, {'label': 'Grand Canyon', 'value': 'Grand Canyon'},
               {'label': 'Green Bay', 'value': 'Green Bay'}, {'label': 'Hampton', 'value': 'Hampton'},
               {'label': 'Hartford', 'value': 'Hartford'}, {'label': 'Harvard', 'value': 'Harvard'},
               {'label': 'Hawaii', 'value': 'Hawaii'}, {'label': 'High Point', 'value': 'High Point'},
               {'label': 'Hofstra', 'value': 'Hofstra'}, {'label': 'Holy Cross', 'value': 'Holy Cross'},
               {'label': 'Houston Baptist', 'value': 'Houston Baptist'}, {'label': 'Houston', 'value': 'Houston'},
               {'label': 'Howard', 'value': 'Howard'}, {'label': 'Idaho State', 'value': 'Idaho State'},
               {'label': 'Idaho', 'value': 'Idaho'}, {'label': 'Illinois-Chicago', 'value': 'Illinois-Chicago'},
               {'label': 'Illinois State', 'value': 'Illinois State'}, {'label': 'Illinois', 'value': 'Illinois'},
               {'label': 'Incarnate Word', 'value': 'Incarnate Word'},
               {'label': 'Indiana State', 'value': 'Indiana State'}, {'label': 'Indiana', 'value': 'Indiana'},
               {'label': 'Iona', 'value': 'Iona'}, {'label': 'Iowa State', 'value': 'Iowa State'},
               {'label': 'Iowa', 'value': 'Iowa'}, {'label': 'Fort Wayne', 'value': 'Fort Wayne'},
               {'label': 'IUPUI', 'value': 'IUPUI'}, {'label': 'Jackson State', 'value': 'Jackson State'},
               {'label': 'Jacksonville State', 'value': 'Jacksonville State'},
               {'label': 'Jacksonville', 'value': 'Jacksonville'}, {'label': 'James Madison', 'value': 'James Madison'},
               {'label': 'Kansas State', 'value': 'Kansas State'}, {'label': 'Kansas', 'value': 'Kansas'},
               {'label': 'Kennesaw State', 'value': 'Kennesaw State'}, {'label': 'Kent State', 'value': 'Kent State'},
               {'label': 'Kentucky', 'value': 'Kentucky'}, {'label': 'La Salle', 'value': 'La Salle'},
               {'label': 'Lafayette', 'value': 'Lafayette'}, {'label': 'Lamar', 'value': 'Lamar'},
               {'label': 'Lehigh', 'value': 'Lehigh'}, {'label': 'Liberty', 'value': 'Liberty'},
               {'label': 'Lipscomb', 'value': 'Lipscomb'}, {'label': 'Long Beach State', 'value': 'Long Beach State'},
               {'label': 'Long Island University', 'value': 'Long Island University'},
               {'label': 'Longwood', 'value': 'Longwood'}, {'label': 'Louisiana', 'value': 'Louisiana'},
               {'label': 'Louisiana-Monroe', 'value': 'Louisiana-Monroe'},
               {'label': 'Louisiana State', 'value': 'Louisiana State'},
               {'label': 'Louisiana Tech', 'value': 'Louisiana Tech'}, {'label': 'Louisville', 'value': 'Louisville'},
               {'label': 'Loyola (IL)', 'value': 'Loyola (IL)'},
               {'label': 'Loyola Marymount', 'value': 'Loyola Marymount'},
               {'label': 'Loyola (MD)', 'value': 'Loyola (MD)'}, {'label': 'Maine', 'value': 'Maine'},
               {'label': 'Manhattan', 'value': 'Manhattan'}, {'label': 'Marist', 'value': 'Marist'},
               {'label': 'Marquette', 'value': 'Marquette'}, {'label': 'Marshall', 'value': 'Marshall'},
               {'label': 'Maryland-Baltimore County', 'value': 'Maryland-Baltimore County'},
               {'label': 'Maryland-Eastern Shore', 'value': 'Maryland-Eastern Shore'},
               {'label': 'Maryland', 'value': 'Maryland'},
               {'label': 'Massachusetts-Lowell', 'value': 'Massachusetts-Lowell'},
               {'label': 'Massachusetts', 'value': 'Massachusetts'},
               {'label': 'McNeese State', 'value': 'McNeese State'}, {'label': 'Memphis', 'value': 'Memphis'},
               {'label': 'Mercer', 'value': 'Mercer'}, {'label': 'Miami (FL)', 'value': 'Miami (FL)'},
               {'label': 'Miami (OH)', 'value': 'Miami (OH)'}, {'label': 'Michigan State', 'value': 'Michigan State'},
               {'label': 'Michigan', 'value': 'Michigan'}, {'label': 'Middle Tennessee', 'value': 'Middle Tennessee'},
               {'label': 'Milwaukee', 'value': 'Milwaukee'}, {'label': 'Minnesota', 'value': 'Minnesota'},
               {'label': 'Mississippi State', 'value': 'Mississippi State'},
               {'label': 'Mississippi Valley State', 'value': 'Mississippi Valley State'},
               {'label': 'Mississippi', 'value': 'Mississippi'},
               {'label': 'Missouri-Kansas City', 'value': 'Missouri-Kansas City'},
               {'label': 'Missouri State', 'value': 'Missouri State'}, {'label': 'Missouri', 'value': 'Missouri'},
               {'label': 'Monmouth', 'value': 'Monmouth'}, {'label': 'Montana State', 'value': 'Montana State'},
               {'label': 'Montana', 'value': 'Montana'}, {'label': 'Morehead State', 'value': 'Morehead State'},
               {'label': 'Morgan State', 'value': 'Morgan State'},
               {'label': "Mount St. Mary's", 'value': "Mount St. Mary's"},
               {'label': 'Murray State', 'value': 'Murray State'}, {'label': 'Navy', 'value': 'Navy'},
               {'label': 'Omaha', 'value': 'Omaha'}, {'label': 'Nebraska', 'value': 'Nebraska'},
               {'label': 'Nevada-Las Vegas', 'value': 'Nevada-Las Vegas'}, {'label': 'Nevada', 'value': 'Nevada'},
               {'label': 'New Hampshire', 'value': 'New Hampshire'},
               {'label': 'New Mexico State', 'value': 'New Mexico State'},
               {'label': 'New Mexico', 'value': 'New Mexico'}, {'label': 'New Orleans', 'value': 'New Orleans'},
               {'label': 'Niagara', 'value': 'Niagara'}, {'label': 'Nicholls State', 'value': 'Nicholls State'},
               {'label': 'NJIT', 'value': 'NJIT'}, {'label': 'Norfolk State', 'value': 'Norfolk State'},
               {'label': 'North Carolina-Asheville', 'value': 'North Carolina-Asheville'},
               {'label': 'North Carolina A&T', 'value': 'North Carolina A&T'},
               {'label': 'North Carolina Central', 'value': 'North Carolina Central'},
               {'label': 'North Carolina-Greensboro', 'value': 'North Carolina-Greensboro'},
               {'label': 'North Carolina State', 'value': 'North Carolina State'},
               {'label': 'North Carolina-Wilmington', 'value': 'North Carolina-Wilmington'},
               {'label': 'North Carolina', 'value': 'North Carolina'},
               {'label': 'North Dakota State', 'value': 'North Dakota State'},
               {'label': 'North Dakota', 'value': 'North Dakota'}, {'label': 'North Florida', 'value': 'North Florida'},
               {'label': 'North Texas', 'value': 'North Texas'}, {'label': 'Northeastern', 'value': 'Northeastern'},
               {'label': 'Northern Arizona', 'value': 'Northern Arizona'},
               {'label': 'Northern Colorado', 'value': 'Northern Colorado'},
               {'label': 'Northern Illinois', 'value': 'Northern Illinois'},
               {'label': 'Northern Iowa', 'value': 'Northern Iowa'},
               {'label': 'Northern Kentucky', 'value': 'Northern Kentucky'},
               {'label': 'Northwestern State', 'value': 'Northwestern State'},
               {'label': 'Northwestern', 'value': 'Northwestern'}, {'label': 'Notre Dame', 'value': 'Notre Dame'},
               {'label': 'Oakland', 'value': 'Oakland'}, {'label': 'Ohio State', 'value': 'Ohio State'},
               {'label': 'Ohio', 'value': 'Ohio'}, {'label': 'Oklahoma State', 'value': 'Oklahoma State'},
               {'label': 'Oklahoma', 'value': 'Oklahoma'}, {'label': 'Old Dominion', 'value': 'Old Dominion'},
               {'label': 'Oral Roberts', 'value': 'Oral Roberts'}, {'label': 'Oregon State', 'value': 'Oregon State'},
               {'label': 'Oregon', 'value': 'Oregon'}, {'label': 'Pacific', 'value': 'Pacific'},
               {'label': 'Penn State', 'value': 'Penn State'}, {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
               {'label': 'Pepperdine', 'value': 'Pepperdine'}, {'label': 'Pittsburgh', 'value': 'Pittsburgh'},
               {'label': 'Portland State', 'value': 'Portland State'}, {'label': 'Portland', 'value': 'Portland'},
               {'label': 'Prairie View', 'value': 'Prairie View'}, {'label': 'Presbyterian', 'value': 'Presbyterian'},
               {'label': 'Princeton', 'value': 'Princeton'}, {'label': 'Providence', 'value': 'Providence'},
               {'label': 'Purdue', 'value': 'Purdue'}, {'label': 'Quinnipiac', 'value': 'Quinnipiac'},
               {'label': 'Radford', 'value': 'Radford'}, {'label': 'Rhode Island', 'value': 'Rhode Island'},
               {'label': 'Rice', 'value': 'Rice'}, {'label': 'Richmond', 'value': 'Richmond'},
               {'label': 'Rider', 'value': 'Rider'}, {'label': 'Robert Morris', 'value': 'Robert Morris'},
               {'label': 'Rutgers', 'value': 'Rutgers'}, {'label': 'Sacramento State', 'value': 'Sacramento State'},
               {'label': 'Sacred Heart', 'value': 'Sacred Heart'},
               {'label': 'Saint Francis (PA)', 'value': 'Saint Francis (PA)'},
               {'label': "Saint Joseph's", 'value': "Saint Joseph's"}, {'label': 'Saint Louis', 'value': 'Saint Louis'},
               {'label': "Saint Mary's (CA)", 'value': "Saint Mary's (CA)"},
               {'label': "Saint Peter's", 'value': "Saint Peter's"},
               {'label': 'Sam Houston State', 'value': 'Sam Houston State'}, {'label': 'Samford', 'value': 'Samford'},
               {'label': 'San Diego State', 'value': 'San Diego State'}, {'label': 'San Diego', 'value': 'San Diego'},
               {'label': 'San Francisco', 'value': 'San Francisco'},
               {'label': 'San Jose State', 'value': 'San Jose State'}, {'label': 'Santa Clara', 'value': 'Santa Clara'},
               {'label': 'Savannah State', 'value': 'Savannah State'}, {'label': 'Seattle', 'value': 'Seattle'},
               {'label': 'Seton Hall', 'value': 'Seton Hall'}, {'label': 'Siena', 'value': 'Siena'},
               {'label': 'South Alabama', 'value': 'South Alabama'},
               {'label': 'South Carolina State', 'value': 'South Carolina State'},
               {'label': 'South Carolina Upstate', 'value': 'South Carolina Upstate'},
               {'label': 'South Carolina', 'value': 'South Carolina'},
               {'label': 'South Dakota State', 'value': 'South Dakota State'},
               {'label': 'South Dakota', 'value': 'South Dakota'}, {'label': 'South Florida', 'value': 'South Florida'},
               {'label': 'Southeast Missouri State', 'value': 'Southeast Missouri State'},
               {'label': 'Southeastern Louisiana', 'value': 'Southeastern Louisiana'},
               {'label': 'Southern California', 'value': 'Southern California'},
               {'label': 'SIU Edwardsville', 'value': 'SIU Edwardsville'},
               {'label': 'Southern Illinois', 'value': 'Southern Illinois'},
               {'label': 'Southern Methodist', 'value': 'Southern Methodist'},
               {'label': 'Southern Mississippi', 'value': 'Southern Mississippi'},
               {'label': 'Southern Utah', 'value': 'Southern Utah'}, {'label': 'Southern', 'value': 'Southern'},
               {'label': 'St. Bonaventure', 'value': 'St. Bonaventure'},
               {'label': 'St. Francis (NY)', 'value': 'St. Francis (NY)'},
               {'label': "St. John's (NY)", 'value': "St. John's (NY)"}, {'label': 'Stanford', 'value': 'Stanford'},
               {'label': 'Stephen F. Austin', 'value': 'Stephen F. Austin'}, {'label': 'Stetson', 'value': 'Stetson'},
               {'label': 'Stony Brook', 'value': 'Stony Brook'}, {'label': 'Syracuse', 'value': 'Syracuse'},
               {'label': 'Temple', 'value': 'Temple'}, {'label': 'Tennessee-Martin', 'value': 'Tennessee-Martin'},
               {'label': 'Tennessee State', 'value': 'Tennessee State'},
               {'label': 'Tennessee Tech', 'value': 'Tennessee Tech'}, {'label': 'Tennessee', 'value': 'Tennessee'},
               {'label': 'Texas A&M-Corpus Christi', 'value': 'Texas A&M-Corpus Christi'},
               {'label': 'Texas A&M', 'value': 'Texas A&M'}, {'label': 'Texas-Arlington', 'value': 'Texas-Arlington'},
               {'label': 'Texas Christian', 'value': 'Texas Christian'},
               {'label': 'Texas-El Paso', 'value': 'Texas-El Paso'},
               {'label': 'Texas-Rio Grande Valley', 'value': 'Texas-Rio Grande Valley'},
               {'label': 'Texas-San Antonio', 'value': 'Texas-San Antonio'},
               {'label': 'Texas Southern', 'value': 'Texas Southern'}, {'label': 'Texas State', 'value': 'Texas State'},
               {'label': 'Texas Tech', 'value': 'Texas Tech'}, {'label': 'Texas', 'value': 'Texas'},
               {'label': 'Toledo', 'value': 'Toledo'}, {'label': 'Towson', 'value': 'Towson'},
               {'label': 'Troy', 'value': 'Troy'}, {'label': 'Tulane', 'value': 'Tulane'},
               {'label': 'Tulsa', 'value': 'Tulsa'}, {'label': 'UCLA', 'value': 'UCLA'},
               {'label': 'Utah State', 'value': 'Utah State'}, {'label': 'Utah Valley', 'value': 'Utah Valley'},
               {'label': 'Utah', 'value': 'Utah'}, {'label': 'Valparaiso', 'value': 'Valparaiso'},
               {'label': 'Vanderbilt', 'value': 'Vanderbilt'}, {'label': 'Vermont', 'value': 'Vermont'},
               {'label': 'Villanova', 'value': 'Villanova'},
               {'label': 'Virginia Commonwealth', 'value': 'Virginia Commonwealth'}, {'label': 'VMI', 'value': 'VMI'},
               {'label': 'Virginia Tech', 'value': 'Virginia Tech'}, {'label': 'Virginia', 'value': 'Virginia'},
               {'label': 'Wagner', 'value': 'Wagner'}, {'label': 'Wake Forest', 'value': 'Wake Forest'},
               {'label': 'Washington State', 'value': 'Washington State'},
               {'label': 'Washington', 'value': 'Washington'}, {'label': 'Weber State', 'value': 'Weber State'},
               {'label': 'West Virginia', 'value': 'West Virginia'},
               {'label': 'Western Carolina', 'value': 'Western Carolina'},
               {'label': 'Western Illinois', 'value': 'Western Illinois'},
               {'label': 'Western Kentucky', 'value': 'Western Kentucky'},
               {'label': 'Western Michigan', 'value': 'Western Michigan'},
               {'label': 'Wichita State', 'value': 'Wichita State'},
               {'label': 'William & Mary', 'value': 'William & Mary'}, {'label': 'Winthrop', 'value': 'Winthrop'},
               {'label': 'Wisconsin', 'value': 'Wisconsin'}, {'label': 'Wofford', 'value': 'Wofford'},
               {'label': 'Wright State', 'value': 'Wright State'}, {'label': 'Wyoming', 'value': 'Wyoming'},
               {'label': 'Xavier', 'value': 'Xavier'}, {'label': 'Yale', 'value': 'Yale'},
               {'label': 'Youngstown State', 'value': 'Youngstown State'}]

app = dash.Dash()
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Dropdown(
                id='year-dropdown',
                options=[
                    {'label': '2018', 'value': '2018'},
                    {'label': '2017', 'value': '2017'},
                    {'label': '2016', 'value': '2016'},
                    {'label': '2015', 'value': '2015'},
                    {'label': '2014', 'value': '2014'}
                ],
                value='2018',
                clearable=False
            ),
            style={'float': 'left', 'width': '10%'}
        ),
        html.Div(
            html.H1(
                children='Team Comparison v1',
                style={'text-align': 'center'}
            )
        )
    ]),
    html.Div([
        html.Div(
            html.Img(id='teamA-logo'),
            style={'float': 'left', 'width': '10%', 'display': 'block', 'margin': 'auto'}
        ),
        html.Div(
            html.Img(id='teamB-logo'),
            style={'float': 'right', 'width': '10%', 'display': 'block', 'margin': 'auto'}
        )
    ],
        style={'width': '80%', 'padding-bottom': 60, 'margin': 'auto'}
    ),
    html.Div([
        html.Div(
            html.H3(id='teamA-record'),
            style={'float': 'left', 'width': '10%', 'text-align': 'center'}
        ),
        html.Div(
            html.H3(id='teamB-record'),
            style={'float': 'right', 'width': '10%', 'text-align': 'center'}
        )
    ],
        style={'width': '80%', 'padding-bottom': 60, 'margin': 'auto'}
    ),
    html.Div([
        html.Div(
            dcc.Dropdown(
                id='teamA',
                options=teamOptions,
                value='West Virginia',
                clearable=False
            ),
            style={'width': 150, 'float': 'left'}
        ),
        html.Div(
            dcc.Dropdown(
                id='teamB',
                options=teamOptions,
                value='Pittsburgh',
                clearable=False
            ),
            style={'width': 150, 'float': 'right'}
        ),
        html.Div(
            html.Div(id='team-stats-table'),
            style={'width': '80%', 'margin': 'auto', 'padding-top': 100}
        )
    ],
        style={'width': '80%', 'margin': 'auto'})
])


@app.callback(dash.dependencies.Output('teamA-record', 'children'),
              [dash.dependencies.Input('year-dropdown', 'value'),
               dash.dependencies.Input('teamA', 'value')])
def getTeamARecord(year, team):
    return collection.find({'_id': year})[0][team]['record']


@app.callback(dash.dependencies.Output('teamB-record', 'children'),
              [dash.dependencies.Input('year-dropdown', 'value'),
               dash.dependencies.Input('teamB', 'value')])
def getTeamBRecord(year, team):
    return collection.find({'_id': year})[0][team]['record']


@app.callback(dash.dependencies.Output('teamA-logo', 'src'),
              [dash.dependencies.Input('year-dropdown', 'value'),
               dash.dependencies.Input('teamA', 'value')])
def getTeamALogo(year, team):
    return collection.find({'_id': year})[0][team]['logo']


@app.callback(dash.dependencies.Output('teamB-logo', 'src'),
              [dash.dependencies.Input('year-dropdown', 'value'),
               dash.dependencies.Input('teamB', 'value')])
def getTeamBLogo(year, team):
    return collection.find({'_id': year})[0][team]['logo']


@app.callback(dash.dependencies.Output('team-stats-table', 'children'),
              [dash.dependencies.Input('year-dropdown', 'value'),
               dash.dependencies.Input('teamA', 'value'),
               dash.dependencies.Input('teamB', 'value')]
              )
def getTeamStatsTable(year, teamA, teamB):
    teamAStats = collection.find({'_id': year})[0][teamA]['teamStats']
    teamBStats = collection.find({'_id': year})[0][teamB]['teamStats']

    allStats = ['fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a', 'fg3_pct',
                'ft', 'fta', 'ft_pct', 'ast', 'pts', 'pts_per_g', 'orb', 'drb', 'trb', 'stl', 'blk', 'tov']
    teamOne = []
    stat = []
    teamTwo = []
    teamOneAdv = []
    teamTwoAdv = []
    for teamStat in allStats:
        teamOneStat = teamAStats[teamStat]['value'] + ' (' + teamAStats[teamStat]['rank'] + ')'
        teamTwoStat = teamBStats[teamStat]['value'] + ' (' + teamBStats[teamStat]['rank'] + ')'

        stat.append(teamStat)
        teamOne.append(teamOneStat)
        teamTwo.append(teamTwoStat)

        teamADiff = re.search('(\d+)', teamOneStat).group(1)
        teamBDiff = re.search('(\d+)', teamTwoStat).group(1)

        if int(teamADiff) > int(teamBDiff):
            diff = int(teamADiff) - int(teamBDiff)
            if teamStat == 'tov':
                teamTwoAdv.append('-' + str(diff))
                teamOneAdv.append(None)
            else:
                teamOneAdv.append('+' + str(diff))
                teamTwoAdv.append(None)
        else:
            diff = int(teamBDiff) - int(teamADiff)
            if teamStat == 'tov':
                teamOneAdv.append('-' + str(diff))
                teamTwoAdv.append(None)
            else:
                teamTwoAdv.append('+' + str(diff))
                teamOneAdv.append(None)

    advA = '{} Diff'.format(teamA)
    advB = '{} Diff'.format(teamB)

    data = {advA: teamOneAdv, teamA: teamOne, 'Stat': stat, teamB: teamTwo, advB: teamTwoAdv}
    df = pd.DataFrame(data)

    return html.Div(
        html.Table(
            [html.Tr([html.Th(col) for col in df.columns])] +
            [html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), len(allStats)))],
            style={'border-spacing': 30, 'margin': 'auto', 'text-align': 'center'}
        )
    )


if __name__ == '__main__':
    app.run_server(debug=True)
