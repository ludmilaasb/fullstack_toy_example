import json
import time
from urllib.parse import urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.yelp.pl"
SEARCH_URL = BASE_URL + "/search?find_desc=Hair+Salons&find_loc=Warszawa"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8",
}

def get_saloon_links():
    resp = requests.get(SEARCH_URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    seen = set()
    for a in soup.find_all("a", href=True, class_="y-css-10p1g8z"):
        href = a["href"]
        if not href.startswith("/biz/"):
            continue
        link_sanitized = urlunparse(
            urlparse(BASE_URL + a["href"])._replace(query="")
        )
        seen.add(link_sanitized)
        time.sleep(1)
    return list(seen)

if __name__ == "__main__":
    links = get_saloon_links()
    for link in links:
        print(link)