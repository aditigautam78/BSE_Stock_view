import cherrypy
import os
from bs4 import BeautifulSoup
import urllib
from io import BytesIO
from zipfile import ZipFile
import redis
import json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('html'))

class HelloWorld(object):

    def get_csv(self):
        url = "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx"

        content = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(content)

        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        resp = urllib.request.urlopen(links[1])
        zipfile = ZipFile(BytesIO(resp.read()))

        df = pd.read_csv((zipfile.open(zipfile.namelist()[0])))
        new = df.filter(['SC_CODE', 'SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE'], axis=1)
        key = 0
        for i in json.loads(new.to_json(orient='records')):
            red.hmset(key, i)

        red = redis.StrictRedis(charset="utf-8", decode_responses=True)
        cursor, possible_keys = red.scan(count=10)

        list = [red.hgetall(items) for items in possible_keys]
        return list

    @cherrypy.expose
    def index(self):
        data_to_show = self.get_csv()
        tmpl = env.get_template('index.html')
        return tmpl.render(data=data_to_show)

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}

cherrypy.quickstart(HelloWorld(), '/', config=config)
