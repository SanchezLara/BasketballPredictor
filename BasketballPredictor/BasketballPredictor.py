
# Getter for all 
def playerrecordsyears(start, end):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    url = []
    soup = []

    for year in range(start,end):
        url.append('https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'.format(year))
        r = requests.get(url[year-start])
        r_html = r.text
        soup.append(BeautifulSoup(r_html,'html.parser'))

        table = []
        for i in soup:
            table.append(i.find_all(class_="full_table"))

    head=soup[1].find(class_="thead")
    column_names_raw=[head.text for item in head][0]
    year_polished = (column_names_raw.replace("\n",",").split(",")[2:-1])
    """ Extracting List of column names"""

    players=[[]]

    for t in range(len(table)):
        players.append([])
        for i in range(len(table[t])):
            player_=[]
            for td in table[t][i].find_all("td"):
                player_.append(td.text)
            players[t].append(player_)

    df = []

    for i in range(len(players)):
        temp = pd.DataFrame(players[i], columns=year_polished).set_index("Player")
        df.append(temp)
        df[i].index=df[i].index.str.replace('*', '')
    return df

data = playerrecordsyears(1990,2015)
