from prompt_builder import prompt
from crawler import get_urls, get_soup_object
from threading import Thread

def crawl_and_clean_document_for_problem(urls, input_string, problem, data):
    is_done = False
    for idx, url in enumerate(urls):
        if is_done:
            break
        print("-"*25 + f"START PROCESSING DOCUMENT {idx}" + "-"*25)
        print(f"URL: {url}") 
        crawl_result = get_soup_object(url)
        if crawl_result["document"]:
            link = crawl_result["url"]
            raw_document = crawl_result["document"]
            title = crawl_result["title"]
            
            print(f"CLEANING DOCUMENT {title}")
            clean_kwargs = {"document": raw_document}
            clean_document = prompt(input=input_string, type="clean", **clean_kwargs)
            if clean_document:
                print("-"*25 + "CLEANED DOCUMENT" + "-"*25)
                print(clean_document)
                data[problem] = {"documents": [clean_document], "links": [link], "titles": [title]}
                is_done = True

def main(input_string):
    # Prompt for search strings
    # response = prompt(input=input_string, type="search")
    # df_document = None
    # for search_string in response[:1]: #For quick testing, just process the first search string 
    #     print(f"Crawling document for {search_string}")
    #     df_document = crawl(search_string=search_string, df_document=df_document, max_doc=1)
    
    problems = prompt(input_string, type="parse")
    problem_urls = {}
    data = {}
    for problem in problems:
        urls = get_urls(text_search=problem, num_of_page=20)
        problem_urls[problem] = urls
        data[problem] = {"documents": [], "links": [], "titles": []}

    threads = [None] * len(problems)
    for idx, problem in enumerate(problems):
        print("-"*25 + f"START PROCESSING PROBLEM" + "-"*25)
        print(problem)
        threads[idx] = Thread(target=crawl_and_clean_document_for_problem, args=(problem_urls[problem], input_string, problem, data))
        threads[idx].start()
        
    for i in range(len(threads)):
        threads[i].join()

    analyze_kwargs = {
        "data": data,
        "problems": problems
    }        
    print("-"*25 + "-"*25)
    result = prompt(input_string, type="analyze", **analyze_kwargs)
    if not result or "INSUFFICIENT" in result:
        pass
    else:
        return result
