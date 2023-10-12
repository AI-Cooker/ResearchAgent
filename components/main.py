from prompt_builder import prompt
from crawler import get_urls, get_soup_object
from parser import parse_page
from db import get_db, find_by_id
import time
import pandas as pd

def main(input_string):
    # Prompt for search strings
    # response = prompt(input=input_string, type="search")
    # df_document = None
    # for search_string in response[:1]: #For quick testing, just process the first search string 
    #     print(f"Crawling document for {search_string}")
    #     df_document = crawl(search_string=search_string, df_document=df_document, max_doc=1)



    # Use input directly
    urls = get_urls(text_search=input_string, num_of_page=10)

    clean_documents = []
    titles = []
    links = []
    for idx, url in enumerate(urls):
        crawl_result = get_soup_object(url)
        try:
            if crawl_result["document"] and url not in links:
                link = crawl_result["url"]
                raw_document = crawl_result["document"]
                title = crawl_result["title"]
                
                print(f"Cleaning document {idx} - {link}")
                clean_kwargs = {"document": raw_document}
                clean_document = prompt(input=input_string, type="clean", **clean_kwargs)
                if clean_document:
                    print(clean_document)
                    clean_documents.append(clean_document)
                    links.append(link)
                    titles.append(title)
                    print(f"Analyzing documents...")
                    analyze_kwargs = {
                        "documents": clean_documents,
                        "links": links,
                        "titles": titles
                    }
                    result = prompt(input_string, type="analyze", **analyze_kwargs)
                    if not result or "INSUFFICIENT" in result:
                        pass
                    else:
                        return result
        except:
            pass
    
        

# input_string = "InsecureRequestWarning: Unverified HTTPS request is being made to host"
input_string = "What are the currently best LLMs, provide a quick comparison between them?"
# input_string = "I have some servers that queries on a single mariadb, one of the server running on highload with high CPU and send a large number of queries to the database, and has very low query response time, but the others still has good response ime, what are the possibly root causes?"
        
        
start = time.time()
res = main(input_string)
# res = prompt(input_string, type="parse")
print("-"*50)
print(res)
print("-"*50)
print(f"Time: {time.time() - start}")

# db = get_db()
# for index, row in df_document.iterrows():
#     db["documents"].insert_one({"prompt": input_string, "title": row["title"], "link": row["link"], "raw_document": row["raw_document"], "clean_document": row["clean_document"]})




# documents = db["documents"]
# res = find_by_id(documents, "6522e907666d033aa0ae07d2")
# print(res)
