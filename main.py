import requests
from bs4 import BeautifulSoup
import sqlite3
import json

url = 'https://quotes.toscrape.com/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

quotes = soup.find_all('span', class_="text")
authors = soup.find_all('small', class_='author')

tags = soup.find_all('div', class_="tags")

some_data = dict()

conn = sqlite3.connect("data_from_web.db")
cursor = conn.cursor()

createSQL = '''CREATE TABLE quotes (author TEXT, quote TEXT, tags TEXT)'''
cursor.execute(createSQL)

SQL = '''INSERT INTO quotes (author, quote, tags) VALUES (?, ?, ?)'''

for i in range(len(quotes)):
    author = authors[i].text
    quote = quotes[i].text
    tag = ', '.join(tags[i].text.split()[1:])
    cursor.execute(SQL, [author, quote, tag])
    conn.commit()

with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(some_data, file)
