import pandas

from collections import defaultdict

from pprint import pprint

import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')


event1 = datetime.datetime(year=1920, month=1, day=1)
event2 = datetime.datetime.now()

delta = event2.year-event1.year

collections = pandas.read_excel('wine2.xlsx', keep_default_na=False).to_dict(orient='records')

products = {}

products_by_categories = collections.defaultdict(collections)
for product in products:
    products_by_categories[product['Категория']].append(product)

pprint(products_by_categories)

def year_correct():
    if delta == 100 or delta >= 105 and delta <= 120:
        return ("лет")
    elif delta == 101:
        return ("год")
    elif delta >= 102 and delta <= 104:
        return ("года")
    else:
        return ("год")



rendered_page = template.render(
    wines=products_by_categories,
    age_company=delta,
    year_text=year_correct()
    )


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
