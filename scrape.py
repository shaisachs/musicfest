import requests
from bs4 import BeautifulSoup

mapurl = 'https://www.somervilleartscouncil.org/porchfest/map/2018'
page = requests.get(mapurl)
soup = BeautifulSoup(page.content, 'html.parser')

div = soup.find('div', class_='view-display-id-panel_pane_11')
tablebody = div.find('table').find('tbody')

for row in tablebody.findAll('tr'):
    cells = row.findAll('td')

    image = cells[0]
    band = cells[1]
    genre = cells[2]
    address = cells[3]
    time = cells[4]



