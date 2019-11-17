import requests
from bs4 import BeautifulSoup
import string
import re
from pymongo import MongoClient
import csv

url = "https://www.rottentomatoes.com/m/star_trek_into_darkness"

response = requests.get(url)


# with open("test.html", mode='wb') as f:
#     f.write(response.content)

my_soup = BeautifulSoup(response.content, "html.parser")


def tomato_rating(soup):
    ratings = soup.find_all("span", {"class": "mop-ratings-wrap__percentage"})
    critic = re.sub("[^0-9]", '', ratings[0].text)
    audience = re.sub("[^0-9]", '', ratings[1].text)
    return critic, audience


def where2watch(soup):
    affiliates = soup.find("ul", {"class": "affiliates__list"})
    items = affiliates.find_all("li", {"class": "affiliate__item"})
    platforms = {}
    for item in items:
        platform = item.a["data-affiliate"]
        if platform in platforms:
            continue
        method = item.a.p.text
        platforms.update({platform: method})
    return platforms


def movie_description(soup):
    description = soup.find("div", {"id": "movieSynopsis"}).text
    return description


def movie_meta(soup):
    meta_data = soup.find_all("li", {"class": "meta-row clearfix"})
    meta = {}
    for data in meta_data:
        label = data.find("div", {"class": "meta-label subtle"})
        value = data.find("div", {"class": "meta-value"})
        meta.update({label.text: value.text.replace("\n", "").replace("  ", "")})
    return meta


def movie_cast(soup):
    casts = soup.find_all("div", {"class": "cast-item media inlineBlock"})
    cast_actor = {}
    counter = 0
    for cast in casts:
        actor = cast.div.a.span["title"]
        acting = cast.find("span", {"class": "characters subtle smaller"})["title"]
        cast_actor.update({counter: [actor, acting]})
        counter += 1
    return cast_actor


def get_movie_name():
    movie_name = []
    with open("movies_metadata.csv", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for item in csv_reader:
            try:
                name = item["title"].lower().replace(' ', '_')
                movie_name.append(name)
            except (AttributeError, ValueError):
                continue
    return movie_name


# client = MongoClient('localhost', 27017)
print(get_movie_name())
