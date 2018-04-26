from bs4 import BeautifulSoup as bs
import requests
import time



"""
Function to get the data from one page of the leaderboard
"""
def get_leaderboarddetails(year,division,scaled,page):
    # Get the endpoint
    request_tosend="https://games.crossfit.com/competitions/api/v1/competitions/open/{}/leaderboards?division={}&region=0&scaled={}&sort=0&occupation=0&page={}".format(year,division,scaled,page)
    # Send the request
    response_data=requests.get(request_tosend).json()
    return response_data



"""
Function to get the data from the page of one athlete
"""
def get_athletesdetails(competitorid):
    dict_athlete={}
    # Get the url
    url_profile="https://games.crossfit.com/athlete/{}".format(competitorid)

    # Get the data from the page
    response=requests.get(url_profile)
    soup = bs(response.content, features="lxml")

    # Select the data in the infobar (details on the athlete)
    infobar=soup.find("ul", {"class": "infobar"})
    # information in the infobar
    if not infobar is None:
        # Get link profile picture
        profile_picture=soup.find("img",{"class":"pic img-circle"})
        dict_athlete['profile_picture_link']=profile_picture["src"]

        #Get name
        name=soup.find("h3",{"class":"c-heading-page-cover"})
        firstname=name.find("small").text
        lastname=name.text.replace(firstname,"").replace("\n","").replace(" ","")
        #print(firstname,lastname)
        dict_athlete['name']=firstname+" "+lastname

        # Get the different columns
        for item in infobar.find_all("li"):
            field=item.find("div",{"class": "item-label"}).text.replace("\n","").replace(" ","").lower()
            dict_athlete[field]=item.find("div",{"class": "text"}).text.replace("\n","").replace(" ","")

        # Get benchmark exercice
        stats=soup.find("ul",{"class": "stats-container"})
        if not stats is None:
            for item in stats.find_all("tr"):
                exercice="bs_"+item.find("th",{"class": "stats-header"}).text.replace("\n","").replace(" ","").lower()
                dict_athlete[exercice]=item.find("td").text.replace("\n","").replace(" ","")
    time.sleep(0.5)
    return dict_athlete

"""
Function to get the data from the page of one athlete
"""
def get_affiliatedetails(affiliateid):
    dict_affiliate={}
    list_param=["country","region","location"]

    url_profile="https://games.crossfit.com/affiliate/{}".format(affiliateid)
    # Get the data from the page
    response=requests.get(url_profile)
    soup = bs(response.content, features="lxml")

    infobar=soup.find("ul", {"class": "infobar"})
    # if there is informations
    if not infobar is None:
        # Get the informatiobs
        for i,elt in enumerate(infobar.find_all("li")[:3]):
            dict_affiliate[list_param[i]]=elt.find_all("div",{"class": "text"})[0].text.replace("\n","").lower().replace("      ","")


        dict_affiliate["name"]=soup.find("h3", {"class": "c-heading-page-cover"}).text


    time.sleep(0.5)
    return dict_affiliate
