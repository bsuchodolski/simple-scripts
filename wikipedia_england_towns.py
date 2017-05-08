from urllib.request import urlopen
import bs4

html = urlopen("https://en.wikipedia.org/wiki/List_of_towns_in_England")
html = html.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

def is_town_table_tr(tag):
    return tag.name == 'tr' and tag.parent['class'] == ['wikitable', 'sortable']

trs = soup.find_all(is_town_table_tr)

towns = '('
for tr in trs:
    if tr.td:
        towns += tr.td.text + '|'
towns = towns[:-1] + ')'

towns_file = open('towns.txt', 'w')
towns_file.write(towns)
towns_file.close()