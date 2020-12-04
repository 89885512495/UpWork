"""
https://www.abokifx.com/ratetypes/?rates=movement

Extract morning, noon, evening rates for NGN EUR and NGN USD
ensure that you return only the day of today.

return json library should look like


{"date": "20201201",
"time": "current",
"eur_buy": "460",
"eur_sell": "470",
"usd_buy": "420",
"usd_sell": "410"}

use pep8
try to keep it all in one file
use subroutines where necessary
we have a lot of additional work for good python and javscript devs
"""


import requests
import json
import time
from bs4 import BeautifulSoup
from agent import user_agent


def get_data():
	"""Get data from page"""
	url = "https://www.abokifx.com/ratetypes/?rates=movement"
	r = requests.get(url, headers=user_agent)
	soup = BeautifulSoup(r.content, 'html.parser')
	table = soup.find_all('tr', class_='table-line')
	for tag in table:

		yield (
			{
				'date': tag.find('td', class_='table-col datalist').get_text(),
				'time': time.strftime("%H:%M"),
				'eur_buy': tag.select('td')[3].get_text(strip=True)[:3],
				'eur_sell': tag.select('td')[3].get_text(strip=True)[5:],
				'usd_buy': tag.select('td')[1].get_text(strip=True)[:3],
				'usd_sell': tag.select('td')[1].get_text(strip=True)[5:],

			}
		)


def get_json():
	"""Get JSON file"""
	data = tuple(get_data())
	with open('abokifx.json', 'w') as file:
		json.dump(data, file, indent=4)


get_json()
