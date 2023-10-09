from bs4 import BeautifulSoup
import requests, json, lxml
from parser import parse_page
import pandas as pd

def crawl(search_string, df_document=None):
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": search_string,  # query example
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

        try:
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
        except:
            pass
        # else:
        #     break
        if page_num == 1:
            break
        
        
    # document_name = "rag"
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
    if df_document is not None:
        for title, link, document in zip(titles, links, documents):
            if link not in df_document["link"].tolist():
                df_document = pd.concat([df_document, pd.DataFrame([{"title": title, "link": link, "raw_document": document}])], ignore_index=True)
    else:
        df_document = pd.DataFrame({"title": titles, "link": links, "raw_document": documents})
    return df_document
# df_document.to_csv(f"components\\data\\documents\\{document_name}.csv")
