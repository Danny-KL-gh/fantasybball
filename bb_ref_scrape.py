import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def scrape_NBA_team_data(years = [2017, 2018]):
    final_df = pd.DataFrame(columns = ['Year','Team','W','L','W/L%',
    'GB','PS/G','PA/G','SRS','Playoffs','Losing_season'])

    for y in years:

        year = y
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

        html = urlopen(url)

        soup = BeautifulSoup(html, features = 'lxml')

        titles = [th.getText() for th in soup.findAll('tr', limit = 2)[0].findAll('th')]

        headers = titles[1:titles.index ('SRS')+1]

        titles = titles[titles.index('SRS')+1]

        try:
            row_titles = titles[0:titles.index('Eastern Conference')]
        
        except: row_titles = titles


        for i in headers:
            row_titles.remove(i)
        row_titles.remove('Western Conference')
        divisions = ['Atlantic Division','Central Division','Southeast Division',
        'Northwest Division','Pacific Division','Southwest Division', 'Midwest Division']

        for d in divisions:
            try:
                row_titles.remove(d)
            except:
                print('No Division: ', d)


        rows = soup.findAll('tr')[1:]
        team_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

        team_stats = [e for e in team_stats if e != []]

        team_stats = team_stats[0:len(row_titles)]

        for i in range(0, len(team_stats)):
            team_stats[i].insert(0, row_titles[i])
            team_stats[i].insert(0, year)

        headers.insert(0, 'Team')
        headers.insert(0, 'Year')

        year_standings = pd.DataFrame(team_stats, columns = headers)

        year_standings['Playoffs'] = ['Y' if '*' in ele else 
        'N' for ele in year_standings['Team']]

        year_standings['Team'] = [ele.replace('*','') for ele in year_standings['Team']]

        year_standings['Losing_season'] = ['Y' if float(ele) < .5 else 
        'N' for ele in year_standings['W/L%']]

        final_df = final_df.append(year_standings)

    print(final_df.info)

    final_df.to_csv('nba_team_data.csv', index=False)