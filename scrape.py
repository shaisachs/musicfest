import requests
from bs4 import BeautifulSoup
import json

def canonicaltime(text):
    if not text:
        return nil

    hour = int(text.upper().replace(':00 PM', '').replace(':30 PM', ''))
    return hour + 12


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

    if not cells:
        continue

    imageCell = cells[0]
    bandInfoCell = cells[1]
    genresCell = cells[2]
    addressCell = cells[3].find(class_='street-address')
    timeCell = cells[4]

    band = {}

    if bandInfoCell and bandInfoCell.a and bandInfoCell.a.string:
        band['name'] = bandInfoCell.a.string

    if bandInfoCell and bandInfoCell.a and bandInfoCell.a['href']:
        bandUrl = bandInfoCell.a['href']

        if bandUrl.startswith('/node'):
            bandUrl = 'https://www.somervilleartscouncil.org' + bandUrl

        band['url'] = bandUrl

    if imageCell and imageCell.a and imageCell.a.img:
        band['image'] = imageCell.a.img['src']

    if band:
        band['@type'] = 'MusicGroup'
        show['performer'] = band
        show['name'] = band['name']

    if addressCell and addressCell.string:
        venue = {}
        venue['@type'] = 'Place'
        venue['address'] = {}
        venue['address']['@type'] = 'PostalAddress'
        venue['address']['streetAddress'] = addressCell.string.strip()
        venue['address']['addressLocality'] = 'Somerville'
        venue['address']['addressRegion'] = 'MA'
        venue['address']['addressCountry'] = 'US'
        show['location'] = venue

    if band and genresCell:
        genres = []
        for genreLink in genresCell.findAll('a'):
            if genreLink and genreLink.string:
                genres.append(genreLink.string)

        show['performer']['genre'] = genres

    if timeCell:
        startTimeDiv = timeCell.find(class_='date-display-start')
        if startTimeDiv and startTimeDiv.string:
            startHour = canonicaltime(startTimeDiv.string)
            show['startDate'] = '2018-05-13T' + str(startHour) + ':00:00-04:00'

    if timeCell:
        endTimeDiv = timeCell.find(class_='date-display-end')
        if endTimeDiv and endTimeDiv.string:
            endHour = canonicaltime(endTimeDiv.string)
            if endHour:
                show['endDate'] = '2018-05-13T' + str(endHour) + ':00:00-04:00'

    show['@context'] = 'http://schema.org/'
    show['@type'] = 'Event'

    shows.append(show)

output = {}
output['shows'] = shows
print json.dumps(output)