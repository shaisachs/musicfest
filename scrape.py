import requests
from bs4 import BeautifulSoup
import json

def canonicaltime(text):
    if not text:
        return nil

    hour = int(text.upper().replace(':00 PM', '').replace(':30 PM', ''))
    return hour + 12


def performerDecorator(cells, resource):
    band = {}

    imageCell = cells[0]
    bandInfoCell = cells[1]
    genresCell = cells[2]

    if bandInfoCell and bandInfoCell.a and bandInfoCell.a.string:
        band['name'] = bandInfoCell.a.string

    if bandInfoCell and bandInfoCell.a and bandInfoCell.a['href']:
        bandUrl = bandInfoCell.a['href']

        if bandUrl.startswith('/node'):
            bandUrl = 'https://www.somervilleartscouncil.org' + bandUrl

        band['url'] = bandUrl

    if imageCell and imageCell.a and imageCell.a.img:
        band['image'] = imageCell.a.img['src']

    if band and genresCell:
        genres = []
        for genreLink in genresCell.findAll('a'):
            if genreLink and genreLink.string:
                genres.append(genreLink.string)

        band['genre'] = genres

    if band:
        band['@type'] = 'MusicGroup'
        resource['performer'] = band

    return resource

def locationDecorator(cells, resource):
    venue = {}

    addressCell = cells[3].find(class_='street-address')

    if addressCell and addressCell.string:
        venue['@type'] = 'Place'
        venue['address'] = {}
        venue['address']['@type'] = 'PostalAddress'
        venue['address']['streetAddress'] = addressCell.string.strip()
        venue['address']['addressLocality'] = 'Somerville'
        venue['address']['addressRegion'] = 'MA'
        venue['address']['addressCountry'] = 'US'

    if venue:
        resource['location'] = venue

    return resource

def timeDecorator(cells, resource):
    timeCell = cells[4]

    if timeCell:
        startTimeDiv = timeCell.find(class_='date-display-start')
        if startTimeDiv and startTimeDiv.string:
            startHour = canonicaltime(startTimeDiv.string)
            resource['startDate'] = '2018-05-13T' + str(startHour) + ':00:00-04:00'

    if timeCell:
        endTimeDiv = timeCell.find(class_='date-display-end')
        if endTimeDiv and endTimeDiv.string:
            endHour = canonicaltime(endTimeDiv.string)
            if endHour:
                resource['endDate'] = '2018-05-13T' + str(endHour) + ':00:00-04:00'

    return resource


def eventDecorator(cells, resource):
    resource = {}

    resource = performerDecorator(cells, resource)
    resource = locationDecorator(cells, resource)
    resource = timeDecorator(cells, resource)

    if resource['performer'] and resource['performer']['name']:
        resource['name'] = resource['performer']['name']

    if resource:
        resource['@context'] = 'http://schema.org/'
        resource['@type'] = 'Event'

    return resource


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

    show = {}

    show = eventDecorator(cells, show)

    if show:
        shows.append(show)

output = {}
output['shows'] = shows
print json.dumps(output)