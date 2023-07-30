import random
import os
import json 

import requests
import yaml
from bs4 import BeautifulSoup

#select random competition results and send list of statistics
#https://www.duosmium.org/data/2023-03-17_NY_states_c.yaml
#https://www.duosmium.org/results/2023-03-17_NY_states_c/ 

#ONLY WORKS FOR SCHOOL RESULTS DUOSMIUM
#addess = link to by school results on Duosmium
#name = name of the school 
def get_competitions(address: str, name: str) -> list[str]:
    competitions = []

    #Download results webpage
    r = requests.get(address)
    if (r.status_code == 404):
        return ["404"]
    
    #Scrape list of invitational links
    page = BeautifulSoup(r.content, "html.parser")
    header_h2 = page.find("h2", id = name)
    ul = header_h2.find_next("ul")
    links = ul.find_all('a')

    #add all competition names to list
    for link in links:
        competitions.append(link['href'].split("/")[2])

    return competitions

#download stauts from duosmium, then process them, only getting stuy results
def update_stats(competitions: list[str], dir: str, key: str) -> None:
    for comp in competitions:
        print("Processing " + comp + "...", end = "")
        address = "https://www.duosmium.org/data/" + comp + ".yaml"

        if (os.path.exists(dir + comp + "/") == False):
            os.mkdir(dir + comp)

            data = requests.get(address)
            y = yaml.safe_load(data.content)

            #Check entries for stuy
            sel_teams = []
            for team in y["Teams"]:
                if (key in team["school"]):
                    sel_teams.append(team)

            #get results of each stuy team
            for team in sel_teams:
                #CURSED AS FUCK
                comp_name = (
                    y["Tournament"].get("name", y["Tournament"]["state"] + " " + y["Tournament"]["level"]) +  
                    " " + str(y["Tournament"]["year"])
                )

                results = {
                    "comp_name" : comp_name, 
                    "year" : y["Tournament"]["year"],
                    "overall_rank" : team["number"],
                    "team_name" : team["school"],
                    "event_rankings" : {}
                }
                #Some tourney results have multiple stuy teams
                if ("suffix" in team.keys()):
                    results["team_name"] += " " + team["suffix"]

                for event in y["Placings"]:
                    if (event["team"] == team["number"]):
                        #if event participation == false, then put the rank as 0
                        results["event_rankings"][event["event"]] = event.get("place", 0)

                with open(dir + comp + "/" + results["team_name"].replace(" ", "_") + ".json", 'w') as wfile:
                    json.dump(results, wfile, indent = 2)
                    wfile.close()

        print("DONE") 
