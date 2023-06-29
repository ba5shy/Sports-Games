import requests
from datetime import datetime
import os
import json
import time 

# main method creates a string with games of the day of selected teams
def main():
    emoji = {
        1: "⚽",
        3: "🏀"
    }

    text = ""
    # check "tomorrow.json" before making API calls
    if not (os.stat("/workspaces/sportsGames/src/data/tomorrow.json").st_size == 0): # check if file is empty
        # if it is not empty, itirate through content
        with open("/workspaces/sportsGames/src/data/tomorrow.json", 'r') as file:
            data = json.load(file)
            for i in data:
                text += i["text"]
    
        # after adding text, delete objects of tomorrow.json (clear file)
        delTomorrow()
    teams = getTeams()
    calls = 0
    tomorrowArray = [] # array of dictionaries to add to tomorrow.json
    for i in teams:
        calls += 1
        response = getResponse(i["id"])
        check = checkResponse(response)
        
        if check[0]:
            if check[3][0]: # if game is tomorrow, add game to "tomorrow.json" file 
                tomorrowText += emoji[check[4]] + " " + check[1] + " - " + check[2] + " " + check[3][1] + "\n"
                toAdd = {"text":tomorrowText}
                tomorrowArray.append(toAdd)
                
            else:
                text += emoji[check[4]] + " " + check[1] + " - " + check[2] + " " + check[3][1] + "\n"
        if calls == 5: # maximum 5 calls per second
            time.sleep(1)
            calls = 0
    if len(tomorrowArray) != 0: # if there are "tomorrow games"
        addTomorrow(tomorrowArray)
    return "No games today" if len(text) == 0 else text

def createURL(teamID):
    url = f'https://sportscore1.p.rapidapi.com/teams/{teamID}/events'
    return url

def getResponse(teamID):
    querystring = {"page":"1"}
    headers = {
	    "X-RapidAPI-Key": "yourAPIKey",
	    "X-RapidAPI-Host": "sportscore1.p.rapidapi.com"
    }

    response = requests.get(createURL(teamID), headers=headers, params=querystring)
    data = response.json()
    return data

def checkResponse(data):
    for i in data['data']:
        if i["start_at"][:10] == str(datetime.now())[:10]:
            start_at = checkTimeZone(i["start_at"][11:16])
            return [True, i["home_team"]["name_code"], i["away_team"]["name_code"],start_at, i["sport_id"]]
    return [False]
    
def getTeams():
    path = os.getcwd() + "/src/data/teams.json"
    file = open(path, 'r')
    data = json.load(file)
    return data

def checkTimeZone(start_at):
    # check api response data against local timezone
    # start_at is the api response
    # 17:00:00 example
    # 23:00 UTC + 3 = 26 - 24 = 2 am
    hours = int(start_at[:2]) + 3
    minutes = start_at[-2:]
    if hours >= 24:
        hours -= 24
        time = "0" + str(hours) + ":" + minutes
        return [True, time]
    else:
        time = str(hours) + ":" + minutes
        return [False, time]

def addTomorrow(array):
    path = "/workspaces/sportsGames/src/data/tomorrow.json"
    with open(path, 'w') as dumpJson:
        json.dump(array, dumpJson, indent=4)

def delTomorrow():
    path = "/workspaces/sportsGames/src/data/tomorrow.json"
    with open(path, 'w') as file:
        file.truncate(0)
