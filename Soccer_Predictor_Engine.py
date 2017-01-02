import urllib.request
import pandas as pd
import numpy as np


"""
Everytime I run this program, I will download the csv file with the latest results.
I will base my analysis on up-to-date results to maximize my prediction engine's accuracy
The csv file will be saved in the same directory as this python file
"""
def downloadLatestCSV():
    #urllib.request.urlretrieve("http://www.football-data.co.uk/mmz4281/1617/E0.csv", "2016-17.csv")
    print("Hi")

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
        #Need to list down matchup here before asking for confirmation
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
#This function calculates how many points HT and AT have won so far
def calculatePoints(teamInfo):
    df = pd.read_csv("2016-17.csv")

    #Calculating points won by HT at home
    homeTeamAtHome_df = df.loc[df["HomeTeam"]==teamInfo[1]]
    homeTeamHomeWins = homeTeamAtHome_df.loc[homeTeamAtHome_df["FTR"]=="H"]
    homeTeamHomeDraws = homeTeamAtHome_df.loc[homeTeamAtHome_df["FTR"]=="D"]
    homeTeamHomePoints = (len(homeTeamHomeWins.index)*3) + (len(homeTeamHomeDraws.index)*1)

    #Calculating points won by HT away from home
    homeTeamAway_df = df.loc[df["AwayTeam"]==teamInfo[1]]
    homeTeamAwayWins = homeTeamAway_df.loc[homeTeamAway_df["FTR"]=="A"]
    homeTeamAwayDraws = homeTeamAway_df.loc[homeTeamAway_df["FTR"]=="D"]
    homeTeamAwayPoints = (len(homeTeamAwayWins.index)*3) + (len(homeTeamAwayDraws.index)*1)

    homeTotalPoints = homeTeamHomePoints + homeTeamAwayPoints # HT total points

    #Calculating points won by AT at home
    awayTeamAtHome_df = df.loc[df["HomeTeam"]==teamInfo[3]]
    awayTeamHomeWins = awayTeamAtHome_df.loc[awayTeamAtHome_df["FTR"]=="H"]
    awayTeamHomeDraws = awayTeamAtHome_df.loc[awayTeamAtHome_df["FTR"]=="D"]
    awayTeamHomePoints = (len(awayTeamHomeWins.index)*3) + (len(awayTeamHomeDraws.index)*1)

    #Calculating points won by AT away form home
    awayTeamAway_df = df.loc[df["AwayTeam"]==teamInfo[3]]
    awayTeamAwayWins = awayTeamAway_df.loc[awayTeamAway_df["FTR"]=="A"]
    awayTeamAwayDraws = awayTeamAway_df.loc[awayTeamAway_df["FTR"]=="D"]
    awayTeamAwayPoints = (len(awayTeamAwayWins.index)*3) + (len(awayTeamAwayDraws.index)*1)

    awayTotalPoints = awayTeamHomePoints + awayTeamAwayPoints # AT total points

    return [homeTotalPoints, awayTotalPoints]


def main():
    downloadLatestCSV()
    teamInfo = processTeamInput() #teamInfo is a list. [homeTeamIndex, homeTeamName, awayTeamIndex, awayTeamName]
    points = calculatePoints(teamInfo) #points[0] = points won by selected home team. points[1] = points won by selected away team


if __name__=="__main__":
    main()