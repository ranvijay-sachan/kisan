import requests
import csv
import re
from lxml import html
from kisanapp.models import ClimateHistory


def download(url):
    r = requests.get(url)
    return r.content


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
    url_data = skip_blank(download(url))
    data = re.sub(' +', ' ', url_data).strip()
    reader = csv.DictReader(data.splitlines(), delimiter=' ')
    l = []
    for row in reader:
        l.append(row)
    return l


def skip_blank(data):
    d = data.find('\n\n')
    return data[d + 1:]


def start():
    base_url = 'http://www.metoffice.gov.uk/climate/uk/summaries/datasets#Yearorder'
    data = get_downloaded_data(base_url)
    for d in data:
        parse_data = parse(d['url'])
        for pr in parse_data:
            if not ClimateHistory.objects.filter(year=int(pr['Year']), temp_type = d['temp_type'],
                                                  region=d['Region']).exists():
                ClimateHistory.objects.create(thread_id=thread, user_id=for_user.pk)

        # obj = ClimateHistory(region='Beatles Blog', temp_type=d['temp_type'],
        #                      month_and_type='', year='', value='', category=d['category'] )
        # obj.save()


if __name__ == '__main__':
    # start()
    print parse('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt')

