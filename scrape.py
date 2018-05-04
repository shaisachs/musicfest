import requests
from bs4 import BeautifulSoup
import json

mapurl = 'https://www.somervilleartscouncil.org/porchfest/map/2018'
page = requests.get(mapurl)
parsedpage = BeautifulSoup(page.content, 'html.parser')

div = parsedpage.find('div', class_='view-display-id-panel_pane_11')
tablebody = div.find('table').find('tbody')

shows = []

i = 0
for row in tablebody.findAll('tr'):
    show = {}

    i += 1
    if i == 1:
        continue

    cells = row.findAll('td')

    image = cells[0]
    band = cells[1]
    genresRaw = cells[2]
    address = cells[3]
    time = cells[4]

    show['bandName'] = band.a.string

    bandUrl = band.a['href']
    if bandUrl.startswith('/node'):
        bandUrl = 'https://www.somervilleartscouncil.org' + bandUrl

    show['bandUrl'] = bandUrl

    if image and image.a and image.a.img:
        show['bandImage'] = image.a.img['src']

    streetaddress = address.find(class_='street-address')

    if streetaddress and streetaddress.string:
        show['streetAddress'] = streetaddress.string.strip()

    genres = []
    for genreRaw in genresRaw.findAll('a'):
        if genreRaw and genreRaw.string:
            genres.append(genreRaw.string)

    show['genres'] = genres

    startTime = time.find(class_='date-display-start')
    if startTime and startTime.string:
        show['startTime'] = startTime.string

    endTime = time.find(class_='date-display-end')
    if endTime and endTime.string:
        show['endTime'] = endTime.string

    shows.append(show)

output = {}
output['shows'] = shows
print json.dumps(output)