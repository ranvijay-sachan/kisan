import requests
import csv
import re
from lxml import html

from models import ClimateHistory


def download(url):
    r = requests.get(url)
    return r.content


def filter_columns(row, col):
    if col is None:
        return row
    return {k: row[k] for k in row if k in col}


def get_downloaded_data(url):
    tree = html.fromstring(download(url))

    for tbody in tree.xpath('//*[@id="wxDetail"]/article/table[2]/tbody'):
        lst = []
        for tr in tbody.xpath('tr'):

            for td in tr.xpath('td'):
                data = {}
                for url in td.xpath("a/@href"):
                    data['url'] = url
                for temp_type in td.xpath("a/@title"):
                    data['temp_type'] = temp_type.rsplit(' ', 1)[1]
                if len(data) > 1:
                    lst.append(data)
                data['category'] = "Year ordered statistics"
                data['Region'] = tr.xpath("td[1]/strong/text()")[0]
        return [i for i in lst if i]


def parse(url):
    col = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT',
           'NOV', 'DEC', 'WIN', 'SPR', 'SUM', 'AUT', 'ANN']
    url_data = skip_blank(download(url))
    data = re.sub(' +', ' ', url_data).strip()
    reader = csv.DictReader(data.splitlines(), delimiter=' ')
    for row in reader:
        year = row.pop('Year', None)
        print row
        row = filter_columns(row, col)
        for month in row:
            c = ClimateHistory()
            c.year = year
            c.month_and_type = month
            c.value = row[month]
            c.region = 'UK'
            c.temp_type = 'Tmax'
            c.category = "test"
            yield c


def skip_blank(data):
    d = data.find('\n\n')
    return data[d + 1:]


def start():
    for p in parse('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt'):
        p.save()
        yield p
    # base_url = 'http://www.metoffice.gov.uk/climate/uk/summaries/datasets#Yearorder'
    # data = get_downloaded_data(base_url)
    # for d in data:
    #     parse_data = parse(d['url'])

# if __name__ == '__main__':
#     start()

    # for p in parse('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt'):
    #     # p.save()
    #     print p

