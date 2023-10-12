import requests
from bs4 import BeautifulSoup
from googlesearch import search  
import re 

def get_urls(text_search, num_of_page=10):
    # to search 
    query = text_search
    
    links = []
    for j in search(query, tld="co.in", num=num_of_page, stop=num_of_page, pause=1): 
        links.append(j) 
    return links

def crawler(url):
    headers = {'content-type': 'application/json',
              'Accept-Language': 'en-US,en;q=0.9',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.content, "lxml")
    title = soup.title.text
    return soup, title


def get_soup_object(url):
    row = {}
    try:
        soup, title = crawler(url)
        row['title'] = title
        row['document'] = re.sub(r"\n\s*\n", "\n", soup.get_text(), flags=re.MULTILINE)
    except Exception as e:
        row['title'] = None
        row['document'] = None
        print('Request error:', e)
    finally:
        row['url'] = url
    return row


def get_soup_objects(text_search, num_of_page):
    data = []
    urls = get_urls(text_search, num_of_page)
    while len(urls) != 0:
        current_url = urls.pop()
        row = {}
        try:
            soup, title = crawler(current_url)
            row['title'] = title
            row['soup'] = re.sub(r"\n\s*\n", "\n", soup.get_text(), flags=re.MULTILINE)
        except Exception as e:
            row['title'] = None
            row['soup'] = None
            print('Request error:', e)
        finally:
            row['url'] = current_url
            data.append(row)
    data_crawler = {text_search: data}
    return data_crawler