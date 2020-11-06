from bs4 import BeautifulSoup
import requests

url = "https://www.imdb.com/chart/top/"
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")
db = []

for i, movie in enumerate(content.find_all("td", attrs={"class": "titleColumn"})):
    print(i + 1)
    print(movie.a.contents)
    for n in movie.stripped_strings:
        print(n)
    print("-" * 80)
