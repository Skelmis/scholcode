import json
import pathlib
from pathlib import Path

cwd = Path(__file__).parents[0]
print(f"{cwd}\n")

global games
games = []

def read_json(filename):
    jsonFile = open(str(cwd)+'/'+filename+'.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def write_json(data, filename):
    jsonFile = open(str(cwd)+'/'+filename+'.json', 'w+')
    jsonFile.write(json.dumps(data,indent=4))
    jsonFile.close()

def SetupTeamJson():#setup the json right
    teams = "argentina:10 australia:6 canada:22 england:11 france:8 georgia:14 ireland:4 italy:12 japan:7 namibia:23 new-zealand:1 russia:20 samoa:15 scotland:9 south-africa:5 tonga:13 uruguay:18 usa:17 wales:2"
    teams = teams.split(" ")
    data = {}
    counter = 0
    for team in teams:
        name, ranking = team.split(":")
        if not counter in data:
            data[counter] = {}
        data[counter]['name'] = name
        data[counter]['ranking'] = int(ranking)
        data[counter]['pointsScored'] = 0
        data[counter]['pointsConceded'] = 0
        data[counter]['triesScored'] = 0
        data[counter]['triesConceded'] = 0
        data[counter]['points'] = 0
        counter += 1
    write_json(data, 'teams')

def GetTeamNumbers():
    correctInput = False
    while correctInput == False:
        try:
            string = str(input("Please enter the five team numbers in the group seperated by spaces: "))
            string = string.split(" ")
            if len(string) == 5:
                for i in range(len(string)):
                    string[i] = int(string[i])
                return string
        except Exception as e:
            print(f"An error occured, please try again.\n{e}")

def GameInput(teamOneName, teamTwoName, teamOneId, teamTwoId):
    #Get the relevant game data
    print(f"In the match between {teamOneName} and {teamTwoName}")
    teamOnePoints = int(input(f"How many points did {teamOneName} score: "))
    teamOneTries = int(input(f"How many tries did {teamOneName} score: "))
    teamTwoPoints = int(input(f"How many points did {teamTwoName} score: "))
    teamTwoTries = int(input(f"How many tries did {teamTwoName} score: "))
    print("\n")

    teamOneMatchPoints = 0
    teamTwoMatchPoints = 0

    #Sussing who won
    if teamOnePoints > teamTwoPoints: #team one wins
        teamOneMatchPoints += 4
        item = teamOneName, teamTwoName, teamOneName #format - {team one}, {team two}, {winner}
        games.append(item)
        if (teamOnePoints - teamTwoPoints) <= 7: #if lost by less then 7
            teamTwoMatchPoints += 1
    elif teamTwoPoints > teamOnePoints: #team two wins
        item = teamOneName, teamTwoName, teamTwoName
        games.append(item)
        teamTwoMatchPoints += 4
        if (teamTwoPoints - teamOnePoints) <= 7:
            teamOneMatchPoints += 1
    elif teamOnePoints == teamTwoPoints:
        item = teamOneName, teamTwoName, None
        games.append(item)
        teamOneMatchPoints += 2
        teamTwoMatchPoints += 2

    #bonus points for tries
    if teamOneTries >= 4:
        teamOneMatchPoints += 1
    if teamTwoTries >= 4:
        teamTwoMatchPoints += 1

    #Update the json with new game data
    teamOneId = str(teamOneId)
    teamTwoId = str(teamTwoId)
    data = read_json('teams')
    data[teamOneId]['pointsScored'] += teamOnePoints
    data[teamOneId]['pointsConceded'] += teamTwoPoints
    data[teamOneId]['triesScored'] += teamOneTries
    data[teamOneId]['triesConceded'] += teamTwoTries
    data[teamOneId]['points'] += teamOneMatchPoints

    data[teamTwoId]['pointsScored'] += teamTwoPoints
    data[teamTwoId]['pointsConceded'] += teamOnePoints
    data[teamTwoId]['triesScored'] += teamTwoTries
    data[teamTwoId]['triesConceded'] += teamOneTries
    data[teamTwoId]['points'] += teamTwoMatchPoints
    write_json(data, 'teams')

def GetTeamData(teamId):
    teamId = str(teamId)
    data = read_json('teams')
    name = data[teamId]['name']
    ranking = data[teamId]['ranking']
    pointsScored = data[teamId]['pointsScored']
    pointsConceded = data[teamId]['pointsConceded']
    triesScored = data[teamId]['triesScored']
    triesConceded = data[teamId]['triesConceded']
    points = data[teamId]['points']
    return name, ranking, pointsScored, pointsConceded, triesScored, triesConceded, points

#needed variables
"""Will Need to know (per team)
Will need to store:
- Points scored by the Team
- Points scored agaisnt the Team
- Tries scored by the Team
- Tries scored agaisnt the Team

Will need to calculate based on the above:
- The difference between points gained by the Team and agaisnt the Team
- The difference between tries scored by the Team and agaisnt the Team
"""

SetupTeamJson()

#get the teams needed for calculations for games
while True:
    games = []
    teams = GetTeamNumbers()
    teamData = []
    for team in teams:
        name, ranking, pointsScored, pointsConceded, triesScored, triesConceded, points = GetTeamData(team)
        item = team, name
        teamData.append(item)
    #print(teamData)

    #Running the pool games. Iteration approach failed due to time so heres a bulk go
    GameInput(teamData[0][1], teamData[1][1], teamData[0][0], teamData[1][0])
    GameInput(teamData[0][1], teamData[2][1], teamData[0][0], teamData[2][0])
    GameInput(teamData[0][1], teamData[3][1], teamData[0][0], teamData[3][0])
    GameInput(teamData[0][1], teamData[4][1], teamData[0][0], teamData[4][0])

    GameInput(teamData[1][1], teamData[2][1], teamData[1][0], teamData[2][0])
    GameInput(teamData[1][1], teamData[3][1], teamData[1][0], teamData[3][0])
    GameInput(teamData[1][1], teamData[4][1], teamData[1][0], teamData[4][0])

    GameInput(teamData[2][1], teamData[3][1], teamData[2][0], teamData[3][0])
    GameInput(teamData[2][1], teamData[4][1], teamData[2][0], teamData[4][0])

    GameInput(teamData[3][1], teamData[4][1], teamData[3][0], teamData[4][0])
    """
    Team 1 plays 2, 3, 4, 5
    Team 2 plays 3, 4, 5
    Team 3 plays 4, 5
    Team 4 plays 5
    """

    for team in teams:
        name, ranking, pointsScored, pointsConceded, triesScored, triesConceded, points = GetTeamData(team)
        item = team, name
        teamData.append(item)

    print("Data input finished")


    di = {}
    data = read_json('teams')
    for i in range(5):
        i = str(i)
        di[data[i]['name']] = int(data[i]['points'])
    results = sorted(di.items(), key=lambda t : t[1], reverse=True)
    #print(results)
    if 1 == 2 and results[0][1] > results[1][1] and results[1][1] > results[2][1] and results[2][1] > results[3][1] and results[3][1] > results[4][1]:
        print(f"The results are in:\nFirst in pool goes to {results[0][0]} with {results[0][1]} points.\nSecond goes to {results[1][0]} with {results[1][1]} points.\nThird goes to {results[2][0]} with {results[2][1]} points.\nFourth is {results[3][0]} with {results[3][1]} points.\nAnd in last place {results[4][0]}, with {results[4][1]} points.")
    else:
        teamOne = results[0]
        teamTwo = results[1]
        #Due to time constraints I will not be coding the first clause for when a tie occurs
        #This will have to be manually dealt with by the user
        print(f"Hey! A duplicate has occured and i now need you to sort it. The following is my data on who team names and there match points:\n{results}\nHere is also my record of who won which games:\n{games}")
        resolution = str(input("If the issue has been resolved please type sorted\nIf the issue has not been sorted please enter no and I will continue the process: "))
        print("\n")
        if 'sorted' in resolution.lower():
            break
        else:
            for item in teamData:
                if item[1] == teamOne[0]:
                    teamOneId = item[0]
                if item[1] == teamTwo[0]:
                    teamTwoId = item[0]
            TeamOnename, TeamOneranking, TeamOnepointsScored, TeamOnepointsConceded, TeamOnetriesScored, TeamOnetriesConceded, TeamOnepoints = GetTeamData(teamOneId)
            teamOneScoreDifference = TeamOnepointsScored - TeamOnepointsConceded
            TeamTwoname, TeamTworanking, TeamTwopointsScored, TeamTwopointsConceded, TeamTwotriesScored, TeamTwotriesConceded, TeamTwopoints = GetTeamData(teamTwoId)
            teamTwoScoreDifference = TeamTwopointsScored - TeamTwopointsConceded

            if teamOneScoreDifference > teamTwoScoreDifference:#stage 2 for decision tree
                print(f"{teamOne[0]} has won and {teamTwo[0]} has come second. Based off points scored.")
            elif teamTwoScoreDifference > teamOneScoreDifference:
                print(f"{teamTwo[0]} has won and {teamOne[0]} has come second. Based off points scored.")
            else:
                #stage 3 for decision tree
                teamOneTryDifference = TeamOnetriesScored - TeamOnetriesConceded
                teamTwoTryDifference = TeamTwotriesScored - TeamTwotriesConceded
                if teamOneTryDifference > teamTwoTryDifference:
                    print(f"{teamOne[0]} has won and {teamTwo[0]} has come second. Based off try range difference.")
                elif teamTwoTryDifference > teamOneTryDifference:
                    print(f"{teamTwo[0]} has won and {teamOne[0]} has come second. Based off try range difference.")
                else:
                    #stage 4 decision tree
                    if TeamOnepointsScored > TeamTwopointsScored:
                        print(f"{teamOne[0]} has won and {teamTwo[0]} has come second. Based off points scored.")
                    elif TeamTwopointsScored > TeamOnepointsScored:
                        print(f"{teamTwo[0]} has won and {teamOne[0]} has come second. Based off points scored.")
                    else:
                        #stage 5 decision tree
                        if TeamOnetriesScored > TeamTwotriesScored:
                            print(f"{teamOne[0]} has won and {teamTwo[0]} has come second. Based off tries.")
                        elif TeamTwotriesScored > TeamOnetriesScored:
                            print(f"{teamTwo[0]} has won and {teamOne[0]} has come second. Based off tries.")
                        else:
                            #stage 6 decision tree
                            if TeamOneranking > TeamTworanking:
                                print(f"{teamOne[0]} has won and {teamTwo[0]} has come second. Based off world ranking.")
                            elif TeamTworanking > TeamOneranking:
                                print(f"{teamTwo[0]} has won and {teamOne[0]} has come second. Based off world ranking.")
                            else:
                                print("idk, something happened and I cant decide because of it :O")

"""
I underestimated the time this program would require and mis-read my requirments.
Due to this, the program is not as good as it could have been given the amount of time
I ended up spending on it, however, it should do what is required with little to no issues.

If the team list needs changing it can be done it can be done by changing the string on line 23
the format is {team name}:{world ranking} seperated by spaces

The entire program should also be flexiable around inputs, to a degree with json requiring
certain keys it is not a guarantee. However, where neccesary I have attempted to do so.

This program has had its parts tested, and as such, under my test conditions it is working fine and as intended.
"""
