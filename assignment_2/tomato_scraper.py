import requests
from bs4 import BeautifulSoup
import string
import re

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
    description = soup.find("div", {"id": "movieSynopsis"})


#critic_per, audience_per = tomato_rating(my_soup)
#print(critic_per)
#print(audience_per)
print(where2watch(my_soup))
