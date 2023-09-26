from bs4 import BeautifulSoup
import requests, json, lxml
from parser import parse_page

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "upgrade mariadb",  # query example
    "hl": "en",  # language
    # "gl": "uk",  # country of the search, UK -> United Kingdom
    "start": 0,  # number page by default up to 0
    # "num": 100          # parameter defines the maximum number of results to return.
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

page_num = 0

data = []

while True:
    page_num += 1
    print(f"page: {page_num}")

    html = requests.get(
        "https://www.google.com/search",
        params=params,
        headers=headers,
        timeout=30,
        verify="D:\\Storages\\certs\\tma-ADCA-CA.crt",
    )
    soup = BeautifulSoup(html.text, "lxml")
    # with open("search_page.html", "w", encoding="utf-8") as f:
    #     f.write(str(html.text))

    for result in soup.select(".tF2Cxc"):
        title = result.select_one(".DKV0Md").text
        try:
            snippet = result.select_one(".lEBKkf span").text
        except:
            snippet = None
        links = result.select_one(".yuRUbf a")["href"]

        data.append({"title": title, "snippet": snippet, "links": links})

    if soup.select_one(".d6cvqb a[id=pnnext]"):
        params["start"] += 10
    # else:
    #     break
    if page_num == 5:
        break

for idx, d in enumerate(data):
    parse_page(d["links"], f"document_{idx}.txt")

print(json.dumps(data, indent=2, ensure_ascii=False))
