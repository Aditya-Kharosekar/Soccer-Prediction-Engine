import urllib.request
import pandas as pd
import numpy as np


"""
Everytime I run this program, I will download the csv file with the latest results.
I will base my analysis on up-to-date results to maximize my prediction engine's accuracy
The csv file will be saved in the same directory as this python file
"""
def downloadLatestCSV():
    urllib.request.urlretrieve("http://www.football-data.co.uk/mmz4281/1617/E0.csv", "2016-17.csv")


"""
The user has to enter the index of the team they want to select.
This function takes that index and converts it to the appropriate team name.
The team name will be used to provide confirmation of the team selected (this will happen in processTeamInput())
"""
def numToNameMapping(num):
    if (num==1):
        return "Arsenal"
    if (num==2):
        return "Bournemouth"
    if (num==3):
        return "Burnley"
    if (num==4):
        return "Chelsea"
    if (num==5):
        return "Crystal Palace"
    if (num==6):
        return "Everton"
    if (num==7):
        return "Hull"
    if (num==8):
        return "Leicester"
    if (num==9):
        return "Liverpool"
    if (num==10):
        return "Man City"
    if (num==11):
        return "Man United"
    if (num==12):
        return "Middlesbrough"
    if (num==13):
        return "Southampton"
    if (num==14):
        return "Stoke"
    if (num==15):
        return "Sunderland"
    if (num==16):
        return "Swansea"
    if (num==17):
        return "Tottenham"
    if (num==18):
        return "Watford"
    if (num==19):
        return "West Brom"
    if (num==20):
        return "West Ham"


"""
Prints out prompts and takes in user's team choices.
Returns a list [homeTeamIndex, homeTeamName, awayTeamIndex, awayTeamName]
"""
def processTeamInput():
    df = pd.read_csv("2016-17.csv")
    names = df["HomeTeam"]
    names = names.drop_duplicates()
    names = names.sort_values(0, True, False, "mergesort", "last") #To sort the team names in alphabetical order
    names = names.tolist() #because I need to iterate through it to print it

    calculate = False;
    while (calculate==False):
        print("Teams: ")
        for num in range(1, 21):
            print(str(num) + " " + names[num-1])

        print("Enter index of home team: ")
        homeIndex = int(input())
        homeName = numToNameMapping(homeIndex)
        print("You have chosen " + homeName + " as the home team")
        print("Enter index of away team: ")
        awayIndex = int(input())
        awayName = numToNameMapping(awayIndex)
        print("You have chosen " + awayName + " as the away team")
        print()
        print(homeName + " vs. " + awayName)
        print("Calculate? (Y/N): ")
        answer = input()
        if (answer=="N" or answer=="n"):
            calculate=False;
            print("Select teams again")
            print()
        else:
            calculate=True;

    return [homeIndex, homeName, awayIndex, awayName] 

#HT = home team as selected by user. AT = away team as selected by user
#This function calculates how many points HT and AT have so far
def calculatePoints(teamInfo):
    df = pd.read_csv("2016-17.csv")

    homeTeam = df[(df["HomeTeam"]==teamInfo[1]) | (df["AwayTeam"]==teamInfo[1])]
    homeTeamWins = homeTeam[((homeTeam["FTR"]=="H") & (homeTeam["HomeTeam"]==teamInfo[1])) | ((homeTeam["FTR"]=="A") & (homeTeam["AwayTeam"]==teamInfo[1]))]
    homeTeamDraws = homeTeam[(homeTeam["FTR"]=="D") & ((homeTeam["HomeTeam"]==teamInfo[1]) | (homeTeam["AwayTeam"]==teamInfo[1]))]

    homeTotalPoints = (len(homeTeamWins.index)*3) + (len(homeTeamDraws.index)*1)

    awayTeam = df[(df["HomeTeam"]==teamInfo[3]) | (df["AwayTeam"]==teamInfo[3])]
    awayTeamWins = awayTeam[((awayTeam["FTR"]=="H") & (awayTeam["HomeTeam"]==teamInfo[3])) | ((awayTeam["FTR"]=="A") & (awayTeam["AwayTeam"]==teamInfo[3]))]
    awayTeamDraws = awayTeam[(awayTeam["FTR"]=="D") & ((awayTeam["HomeTeam"]==teamInfo[3]) | (awayTeam["AwayTeam"]==teamInfo[3]))]

    awayTotalPoints = (len(awayTeamWins.index)*3) + (len(awayTeamDraws.index)*1)

    return [homeTotalPoints, awayTotalPoints]


#This function will calculate the average goals scored per game by HT and AT
#Will return a list. First element - average goals scored per game by HT
#Second element - average goals scored per game by AT
def goalsScoredPerGame(teamInfo):
    df = pd.read_csv("2016-17.csv")

    goals1 = df[df["HomeTeam"]==teamInfo[1]]
    goals2 = df[df["AwayTeam"]==teamInfo[1]]
    homeAvg = (goals1["FTHG"].sum() + goals2["FTAG"].sum()) / (len(goals1.index) + len(goals2.index))

    goals3 = df[df["HomeTeam"]==teamInfo[3]]
    goals4 = df[df["AwayTeam"]==teamInfo[3]]
    awayAvg = (goals3["FTHG"].sum() + goals4["FTAG"].sum()) / (len(goals3.index) + len(goals4.index))

    return [round(homeAvg, 2), round(awayAvg, 2)] #Rounding off the averages to 2 decimal places

#This function will calculate the average goals conceded per game by HT and AT
#Will return a list. First element - average goals conceded per game by HT
#Second element - average goals conceded per game by AT
def goalsConcededPerGame(teamInfo):
    df = pd.read_csv("2016-17.csv")

    goals1 = df[df["HomeTeam"]==teamInfo[1]]
    goals2 = df[df["AwayTeam"]==teamInfo[1]]
    homeAvg = (goals1["FTAG"].sum() + goals2["FTHG"].sum()) / (len(goals1.index) + len(goals2.index))

    goals3 = df[df["HomeTeam"]==teamInfo[3]]
    goals4 = df[df["AwayTeam"]==teamInfo[3]]
    awayAvg = (goals3["FTAG"].sum() + goals4["FTHG"].sum()) / (len(goals3.index) + len(goals4.index))

    return [round(homeAvg, 2), round(awayAvg, 2)] #Rounding off the averages to 2 decimal places


#This function determines how accurate/'efficient with its shots each team is. For both HT and AT, it calculates the following - 
# (goals scored at home + goals scored away) / (shots at home + shots away)
# Returns the percentage
def accuracyGoalsScored(teamInfo):
    df = pd.read_csv("2016-17.csv")

    accuracy1 = df[df["HomeTeam"]==teamInfo[1]]
    accuracy2 = df[df["AwayTeam"]==teamInfo[1]]
    homeAccuracy = (accuracy1["FTHG"].sum() + accuracy2["FTAG"].sum()) / (accuracy1["HS"].sum() + accuracy2["AS"].sum())
    homeAccuracy = homeAccuracy*100; # I want the percentage

    accuracy3 = df[df["HomeTeam"]==teamInfo[3]]
    accuracy4 = df[df["AwayTeam"]==teamInfo[3]]
    awayAccuracy = (accuracy3["FTHG"].sum() + accuracy4["FTAG"].sum()) / (accuracy3["HS"].sum() + accuracy4["AS"].sum())
    awayAccuracy = awayAccuracy*100;

    return [round(homeAccuracy, 2), round(awayAccuracy, 2)]

#This function aims to quantify the quality of the shots that each team concedes. Calculates the following - 
# (goals conceded at home + goals conceded away) / (shots given up at home + shots given up away)
# Returns the percentage
def accuracyGoalsConceded(teamInfo):
    df = pd.read_csv("2016-17.csv")

    accuracy1 = df[df["HomeTeam"]==teamInfo[1]]
    accuracy2 = df[df["AwayTeam"]==teamInfo[1]]
    homeAccuracy = (accuracy1["FTAG"].sum() + accuracy2["FTHG"].sum()) / (accuracy1["AS"].sum() + accuracy2["HS"].sum())
    homeAccuracy = homeAccuracy*100; # I want the percentage

    accuracy3 = df[df["HomeTeam"]==teamInfo[3]]
    accuracy4 = df[df["AwayTeam"]==teamInfo[3]]
    awayAccuracy = (accuracy3["FTAG"].sum() + accuracy4["FTHG"].sum()) / (accuracy3["AS"].sum() + accuracy4["HS"].sum())
    awayAccuracy = awayAccuracy*100;

    return [round(homeAccuracy, 2), round(awayAccuracy, 2)]

#This function quantifies how good HT is at home games and how good AT is at away games
#Returns a list. First element - % of available points that HT has won at home
#Second element - % of available points that AT has won away from home
def getHomeFieldAdvantage(teamInfo):
    df = pd.read_csv("2016-17.csv")

    home = df[df["HomeTeam"]==teamInfo[1]]
    homeWins = home[home["FTR"]=="H"]
    homeDraws = home[home["FTR"]=="D"]
    homePoints = (len(homeWins.index)*3) + (len(homeDraws.index*1))
    homePercentage = (homePoints / (len(home.index)*3))*100 #Multiplying by 100 because I want the percentage

    away = df[df["AwayTeam"]==teamInfo[3]]
    awayWins = away[away["FTR"]=="A"]
    awayDraws = away[away["FTR"]=="D"]
    awayPoints = (len(awayWins.index)*3) + (len(awayDraws.index)*1)
    awayPercentage = (awayPoints / (len(away.index)*3))*100

    return [round(homePercentage, 2), round(awayPercentage, 2)]


def main():
    downloadLatestCSV()
    cont = "Y"
    while (cont=="Y" or cont=="y"):

        teamInfo = processTeamInput() #teamInfo is a list. [homeTeamIndex, homeTeamName, awayTeamIndex, awayTeamName]

        points = calculatePoints(teamInfo) #points[0] = points won by selected home team. points[1] = points won by selected away team
        goalsScored = goalsScoredPerGame(teamInfo)
        goalsConceded = goalsConcededPerGame(teamInfo)
        scoringAccuracy = accuracyGoalsScored(teamInfo)
        defenseEfficiency = accuracyGoalsConceded(teamInfo)
        homeFieldAdvantage = getHomeFieldAdvantage(teamInfo)

        homeScore = 0
        awayScore = 0

        #Points
        if (points[0] > points[1]):
            homeScore +=200
            awayScore += (points[1]/points[0])*200
        else:
            awayScore+=200
            homeScore = (points[0]/points[1])*200

        #Goals scored/game
        if (goalsScored[0] > goalsScored[1]):
            homeScore+=150
            awayScore+=(goalsScored[1]/goalsScored[0])*150
        else:
            homeScore+=(goalsScored[0]/goalsScored[1])*150
            awayScore+=150

        #Goals conceded/game
        if (goalsConceded[0] > goalsConceded[1]):
            awayScore+=150
            homeScore+=150/(goalsConceded[0]/goalsConceded[1])
        else:
            homeScore+=150
            awayScore+=150/(goalsConceded[1]/goalsConceded[0])

        #Goal-scoring efficiency
        if (scoringAccuracy[0] > scoringAccuracy[1]):
            homeScore+=150
            awayScore+=(scoringAccuracy[1]/scoringAccuracy[0])*150
        else:
            homeScore+=(scoringAccuracy[0]/scoringAccuracy[1])*150
            awayScore+=150

        #Defending efficiency
        if (defenseEfficiency[0] > defenseEfficiency[1]):
            awayScore+=150
            homeScore+=150/(defenseEfficiency[0]/defenseEfficiency[1])
        else:
            homeScore+=150
            awayScore+=150/(defenseEfficiency[1]/defenseEfficiency[0])

        #Home field advantage
        if (homeFieldAdvantage[0] > homeFieldAdvantage[1]):
            homeScore+=200
            awayScore+=(homeFieldAdvantage[1]/homeFieldAdvantage[0])*200
        else:
            homeScore+=(homeFieldAdvantage[0]/homeFieldAdvantage[1])*200
            awayScore+=200

        x = 100/(homeScore+awayScore)
        homeWinPerc = homeScore*x;
        awayWinPerc = awayScore*x

        print(teamInfo[1] + " has a " + str(round(homeWinPerc, 2)) + "% chance of winning")
        print(teamInfo[3] + " has a " + str(round(awayWinPerc, 2)) + "% chance of winning")
        if (abs(homeWinPerc-awayWinPerc) < 6):
            print("This is a close game. I predict this game will be a draw")

        print("Continue?(Y/N): ")
        cont = input()

if __name__=="__main__":
    main()