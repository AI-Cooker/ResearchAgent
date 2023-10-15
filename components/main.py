from prompt_builder import prompt
from crawler import get_urls, get_soup_object
from vector_chromadb import check_already_in_db, get_or_create_collection, update_or_insert_to_collection

from threading import Thread

def crawl_and_clean_document_for_problem(urls, input_string, problem, data, collection):
    result, distance = check_already_in_db(problem, collection)
    if result and distance < 10:
        print("Exist in chromadb")
        data[problem] = {"documents": result["documents"], "links": result["links"], "titles": result["titles"]}
        return
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
                update_or_insert_to_collection(data[problem], collection)
                is_done = True

def main(input_string, session_id):
    collection = get_or_create_collection(session_id)
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
        threads[idx] = Thread(target=crawl_and_clean_document_for_problem, args=(problem_urls[problem], input_string, problem, data, collection))
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
