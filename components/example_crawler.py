from bs4 import BeautifulSoup
import requests, json, lxml
from parser import parse_page
import pandas as pd

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": "What is retrieval augmented generation?",  # query example
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
        verify=False,
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

        data.append({"title": title, "snippet": snippet, "link": links})

    if soup.select_one(".d6cvqb a[id=pnnext]"):
        params["start"] += 10
    # else:
    #     break
    if page_num == 5:
        break
    
    
document_name = "rag"
documents = []
titles = []
links = []
snippets = []
org_links = [d["link"] for d in data]
print(f"Number of documents: {len(org_links)}")

for idx, link in enumerate(org_links):
    print(f"Parsing document {idx}: {link}")
    try:
        new_document = parse_page(link)
        documents.append(new_document)
        links.append(link)
        titles.append(data[idx]["title"])
        snippets.append(data[idx]["snippet"])
    except:
        pass
print("Done!")

df_document = pd.DataFrame({"title": titles, "snippet": snippets, "links": links, "raw_document": documents})
df_document.to_csv(f"components\\data\\documents\\{document_name}.csv")
