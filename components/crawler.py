import re 
from bs4 import BeautifulSoup
from googlesearch import search  
from goose3 import Goose


def get_urls(text_search, num_of_page=10):
    # to search 
    query = text_search
    
    links = []
    for j in search(query, tld="co.in", num=num_of_page, stop=num_of_page, pause=1): 
        links.append(j) 
    return links

def crawler(url):    
    g = Goose()
    article = g.extract(url)
    soup = BeautifulSoup(article.raw_html, "lxml")
    title = soup.title.text
    return article.cleaned_text, title


def get_soup_object(url):
    row = {}
    try:
        cleaned_text, title = crawler(url)
        row['title'] = title
        lines = re.sub(r"\n\s*\n", "\n", cleaned_text, flags=re.MULTILINE)
        lines = "".join(lines)
        lines = lines.split("\n")
        lines = "\n".join([line for line in lines if len(line.strip().split(" ")) > 15])
        row['document'] = lines
    except Exception as e:
        row['title'] = None
        row['document'] = None
        print('Cannot crawl the page content: ', e)
    finally:
        row['url'] = url
    return row
