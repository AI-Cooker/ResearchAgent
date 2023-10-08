from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv
import sys
import json


def get_urls(text_search, num_of_page=10):
    # to search
    query = text_search

    links = []
    for j in search(query, tld="co.in", num=num_of_page, stop=num_of_page, pause=1):
        links.append(j)
    return links


def crawler(url):
    headers = {
        "content-type": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.content, "lxml")
    text_data = soup.text
    raw_data = soup
    return text_data, raw_data


def store_url_text(text_search, num_of_page):
    data = []
    urls = get_urls(text_search, num_of_page)
    while len(urls) != 0:
        current_url = urls.pop()
        row = {}
        text_data, raw_data = crawler(current_url)
        row["url"] = current_url
        row["text_data"] = text_data
        # row['raw_data'] = raw_data
        data.append(row)
    data_crawler = {text_search: data}
    with open("crawler.json", "a") as fp:
        json.dump(data_crawler, fp)


store_url_text("python", 5)
# How to use this:
# with open('crawler.json', 'r') as data_crawler:
#     x = json.load(data_crawler)
#    print(x['python'][0]['text_data'])
