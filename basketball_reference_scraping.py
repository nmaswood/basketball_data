#from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import html5lib 
import re

try:
    from  urllib.request import urlopen

except ImportError:

    from urllib2 import urlopen

    

#url='http://www.basketball-reference.com/teams/ATL/2016.html'

#tbody = html_result.select("#div_per_poss > #per_poss > tbody")



def get_team_urls():

    url = "http://www.basketball-reference.com/teams/?lid=front_qi_teams"
    html = urlopen(url)

    bs_obj = BeautifulSoup(html, "lxml")

    href_teams =  bs_obj.select("#active > tbody > tr > td > a")

    teams_list = list()

    for team in href_teams:

        url = team.get("href")
        url = "http://www.basketball-reference.com" + url

        teams_list.append({
        "team_name" : team.get("href"),
        "url" : url
        })

    return teams_list

#print get_team_urls()


teamurl='http://www.basketball-reference.com/teams/MEM/'

def get_team_year_url(teamurl):

    html = urlopen(teamurl)
    bs_obj = BeautifulSoup(html, "lxml")

    my_div =  bs_obj.findAll("div", { "class" : "table_container" })[0] #sort by table container, because do not want to hardcode


    urls =  filter(lambda x: x.get("align") == "left" ,my_div.select("tbody > tr > td")) #keep only urls that are left aligned
    urls =  map(lambda x: x.select("a"), urls) #get a tags
    urls =  filter(lambda x : x != [], urls ) #remove blanks
    urls =  filter(lambda x: "team" in x[0].get("href"), urls) #only get urls with team in them
    urls =  filter(lambda x: "-" in x[0].text, urls) #only get with dash 
    urls =  map (lambda x: x[0], urls) #first element
    urls =  map (lambda x: x.get("href"), urls) #get href from anchor tag
    urls =  filter (lambda x : int((x.split("/"))[-1].split(".")[0]) >= 1990, urls)
    urls =  map (lambda x: "http://www.basketball-reference.com/" + x, urls)

    return urls


#print get_team_year_url(teamurl)
#for index, d in enumerate(data):
#    print d






def playerdata(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html5lib")

    ####advanced
    advanced=soup.find('table', id='advanced') #search for advanced
    column_names=[th.getText() for th in advanced.findAll('th')] #get columns
    data_rows=advanced.findAll('tr')[1:]
    player_data = []  # create an empty list to hold all the data
    for i in range(len(data_rows)):  # for each table row
        player_row = []  # create an empty list for each pick/player
        for td in data_rows[i].findAll('td'): # for each table data element from each table row       
            player_row.append(td.getText())  # get the text content and append to the player_row
        player_data.append(player_row) # then append each pick/player to the player_data matrix
    df = pd.DataFrame(player_data, columns=column_names)
    #df = df.convert_objects(convert_numeric=True)
    advanced=df.drop(['Rk','',''], axis='columns')

    ####pergame
    pergame=soup.find('table', id='per_game') #search for pergame
    column_names=[th.getText() for th in pergame.findAll('th')] #get columns
    data_rows=pergame.findAll('tr')[1:]
    player_data = []  # create an empty list to hold all the data
    for i in range(len(data_rows)):  # for each table row
        player_row = []  # create an empty list for each pick/player
        for td in data_rows[i].findAll('td'): # for each table data element from each table row       
            player_row.append(td.getText())  # get the text content and append to the player_row
        player_data.append(player_row) # then append each pick/player to the player_data matrix
    df = pd.DataFrame(player_data, columns=column_names)
    #df = df.convert_objects(convert_numeric=True)
    pergame=df.drop(['Age','G','MP'],axis='columns')

    ####salaries
    salaries=soup.find('table', id='salaries') #search for salaries
    column_names=[th.getText() for th in salaries.findAll('th')] #get columns
    data_rows=salaries.findAll('tr')[1:]
    player_data = []  # create an empty list to hold all the data
    for i in range(len(data_rows)):  # for each table row
        player_row = []  # create an empty list for each pick/player
        for td in data_rows[i].findAll('td'): # for each table data element from each table row       
            player_row.append(td.getText())  # get the text content and append to the player_row
        player_data.append(player_row) # then append each pick/player to the player_data matrix
    df = pd.DataFrame(player_data, columns=column_names)
    #df = df.convert_objects(convert_numeric=True)
    salaries=df.drop(['Rk'],axis='columns')
    for i in range(len(salaries['Salary'])): #remove punctuation from salarie
        salaries['Salary'][i]=re.sub('[\$,]', '', salaries['Salary'][i])

    playerstats=pd.merge(pd.merge(advanced, pergame, on='Player'),salaries,on='Player')
    return playerstats

#### team ratings
def teamdata(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html5lib")
    teamstats=salaries=soup.find('table', id='team_misc') #search for salaries
    column_names=[th.getText() for th in teamstats.findAll('th')][5:] #get columns from second row
    data_rows=teamstats.findAll('tr')[2:]
    player_data = []  # create an empty list to hold all the data
    for i in range(len(data_rows)):  # for each table row
        player_row = []  # create an empty list for each pick/player
        for td in data_rows[i].findAll('td'): # for each table data element from each table row       
            player_row.append(td.getText())  # get the text content and append to the player_row
        player_data.append(player_row) # then append each pick/player to the player_data matrix
    df = pd.DataFrame(player_data, columns=column_names)
    #df = df.convert_objects(convert_numeric=True)
    teamstats=df.drop(['PW','PL','MOV','SOS','SRS','Arena','Attendance'],axis='columns')
    return teamstats


print playerdata("http://www.basketball-reference.com//teams/VAN/1996.html")






