from bs4 import BeautifulSoup
import requests
import sqlite3

db = sqlite3.connect("movie_ratings.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS movies "
           "(number INTEGER, "
           "title TEXT PRIMARY KEY NOT NULL, "
           "year INTEGER NOT NULL, "
           "rating INTEGER NOT NULL)")

url = "https://www.imdb.com/chart/top/"
response = requests.get(url, timeout=5)
# 200 code means everything went ok. 404 means the page wasn't found.
print(response.status_code)
# print(response.headers)
content = BeautifulSoup(response.content, "html.parser")
# prints formatted html code
# print(content.prettify())
title = []
year = []
rating = []
# finds all the lines with `td` tags with `titleColumn` in the name
links = content.find_all("td")
for line in links:
    # print(line.attrs)
    # looks in the line with class='titleColumn'
    if line["class"] == ["titleColumn"]:
        a_tag = line.find("a")
        span = line.find("span")
        title.append(a_tag.string)
        year.append(span.string)
        # print("-" * 80)
    elif line["class"] == ["ratingColumn", "imdbRating"]:
        s_tag = line.find("strong")
        rating.append(s_tag.string)

# puts all of the scraped data into a sqlite database.
cursor = db.execute("SELECT * FROM movies")
for i in range(1, len(title) + 1):
    cursor.execute("INSERT INTO movies VALUES(?, ?, ?, ?)"
               , (i, title[i - 1], year[i - 1], rating[i - 1]))
    cursor.connection.commit()

db.close()
