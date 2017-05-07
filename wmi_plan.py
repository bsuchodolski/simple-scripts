#! /usr/bin/python3

import requests, bs4, pprint, re

URL = 'https://zajecia.wmi.amu.edu.pl/plan_zaoczne/PlanZaoczne.aspx'

def create_form_data(studia='', rok_studiow='', semestr='',
                     przedmiot='', prowadzacy='', od='', do=''):
    form_data = {
        '__VIEWSTATE': '/wEPDwUKMTI2MDMzNDkzMw9kFgICAw88KwALAGRkmjN9y/JUmvbPY'
                       'fNFmc3wobLvA6Fz1tHPrKiQDpPorsA=',
        '__STATEGENERATOR': 'E977E3D7',
        '__EVENTVALIDATION': '/wEdABemX5Ei7Vj9XvKqm4un/gMyCquxE7SNF6Ev/GjCD3j'
                             'AZoD24HBADxqSI7ixx7suY0tHw2QDrM6NtvhZWbmCAZg1fl'
                             'KN3Ua/42Kz0SJ6yyVrre8Y5E7Fk9X88CqbRfHIRr8g5oH1E'
                             'yJrlQ7ApWalHgzw+uCzpEf8eDCpXTgjL0tjA5OKbT7LN0vP'
                             'PnZT57+PPmJGyolEuA97T/1ylaQQMw4Ru94YU7YEsxuG0U4'
                             'xJ19NOlSLZ57jSulZyKpmZa0tigEQtPgXODcz3FdDeindeg'
                             '7Wp8a5wzQevkQSShpzUKtiPfyM1Zu9cyptVakAamhKNhNcE'
                             'N8d795vtvCxyIcpkCObw5rQIw2Vq4hjgk287/mZvK6q3PoF'
                             'uKWhw3PA5mVNLPY2HUpDx0hule5M5fktkWyMfEiiLvYHH5e'
                             '2e994tkte/EG8Um2lVGFXkSoULFLrPnn2e5bTOaF/X8KHiE'
                             'IFoVmdzfg78Z8BXhXifTCAVkevd94UbXsy9eNiK27eXnT1y'
                             'jBzwdGRWcZ1Ix1b85MIXWEl',
        'Studia': studia,
        'RokStudiow': rok_studiow,
        'Semestr': semestr,
        'Przedmiot': przedmiot,
        'Prowadzacy': prowadzacy,
        'datepicker1': od,
        'datepicker2': do,
        'Button1': 'Szukaj'
    }

    return form_data

def parse_data(studia='', rok_studiow='', semestr='',
                     przedmiot='', prowadzacy='', od='', do=''):

    form_data = create_form_data(studia, rok_studiow, semestr, przedmiot,
                                 prowadzacy, od, do)
    res = requests.post(URL, data=form_data)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    data_table = soup.find_all('tr')

    reg = re.compile(r'(\w*?)\s(\d[A-Z]{2})\s-\s(.*)')

    zajecia = []
    for index, row in enumerate(data_table):
        columns = row.find_all('td')
        zajecia.append({})
        data = zajecia[index] = {}

        data['data'] = columns[0].text
        data['od'] = columns[1].text
        data['sala1'] = columns[2].text
        if columns[3].text == '\xa0':
            data['sala2'] = ''
        else:
            data['sala2'] = columns[3].text
        przedmiot = reg.search(columns[4].text)
        if przedmiot == None:
            continue
        przedmiot = przedmiot.groups()
        data['kod'] = przedmiot[0]
        data['grupa'] = przedmiot[1]
        data['przedmiot'] = przedmiot[2]
        data['prowadzacy'] = columns[5].text
        data['do'] = columns[7].text

    del zajecia[0]
    return zajecia

drugi_rok = parse_data(studia='ZL-INF', rok_studiow='2', semestr='2017L', od='2016-10-01')

for row in drugi_rok:
    if row['grupa'] == '1CB':
        continue
    typ_zajec = ''
    if row['grupa'].startswith('1W'):
        typ_zajec = '- Wykład'
    else:
        typ_zajec = '- Ćwiczenia'
    print(' '.join([row['data'], row['od'], row['przedmiot'], typ_zajec]))

print(pprint.pformat(drugi_rok))