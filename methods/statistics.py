import random

import requests
from bs4 import BeautifulSoup

#select random competition results and send list of statistics
#https://www.duosmium.org/data/2023-03-17_NY_states_c.yaml
#https://www.duosmium.org/results/2023-03-17_NY_states_c/ 

#ONLY WORKS FOR SCHOOL RESULTS DUOSMIUM
def get_competitions(link: str, name: str):
    competitions = []

    #Download results webpage
    r = requests.get(link)
    if (r.status_code == 404):
        return "INVALID_LINK"
    
    #Scrape list of invitational links
    page = BeautifulSoup(r.content, "html.parser")
    header_h2 = page.find("h2", id = name)
    ul = header_h2.find_next("ul")
    links = ul.find_all('a')

    #add all competition names to list
    for link in links:
        competitions.append(link.split("/")[2])

    return competitions

    


