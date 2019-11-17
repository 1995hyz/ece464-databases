import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
import csv

url_prefix = "https://www.rottentomatoes.com/m/"


# with open("test.html", mode='wb') as f:
#     f.write(response.content)


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


def movie_scrapper():
    movies = get_movie_name()
    client = MongoClient('localhost', 27017)
    db = client["rottentomatoes"]
    posts = db.posts
    for movie in movies:
        url = url_prefix + movie
        response = requests.get(url)
        my_soup = BeautifulSoup(response.content, "html.parser")
        critic_per, audience_per = tomato_rating(my_soup)
        media_platform = where2watch(my_soup)
        description = movie_description(my_soup)
        movie_actors = movie_cast(my_soup)
        meta_data = movie_meta(my_soup)
        post_data = {
            "title": movie,
            "tomato_meter": critic_per,
            "audience_score": audience_per,
            "media": media_platform,
            "description": description,
            "major_cast": movie_actors,
            "movie_info": meta_data
        }
        result = posts.insert_one(post_data)
        print('One Post: {0}'.format(result.inserted_id))


if __name__ == "__main__":
    movie_scrapper()