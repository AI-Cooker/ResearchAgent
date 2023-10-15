import time
from .prompt_builder import prompt
from .crawler import get_urls, get_soup_object
from .vector_chromadb import check_already_in_db, get_or_create_collection, update_or_insert_to_collection


def main(input_string, session_id):
    collection = get_or_create_collection(session_id)
    problems = prompt(input_string, type="parse")
    problem_urls = {}
    data = {}
    for problem in problems:
        urls = get_urls(text_search=problem, num_of_page=10)
        problem_urls[problem] = urls
        data[problem] = {}

    for problem in problems:
        print("-"*25 + f"START PROCESSING PROBLEM" + "-"*25)
        print(problem)
        # ----------------------------------------------------
        result, distance = check_already_in_db(problem, collection)
        if result and distance < 10:
            print("Exist in chromadb")
            data[problem] = {"documents": result["documents"], "links": result["links"], "titles": result["titles"]}
            continue
        # ----------------------------------------------------
        is_done = False
        for idx, url in enumerate(problem_urls[problem]):
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
                    data[problem] = {"documents": [clean_document], "links": [link], "titles": [title]}
                    update_or_insert_to_collection(data[problem], collection)
                    is_done = True
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
    

if __name__ == "__main__":
    # input_string =  "What are the currently best LLMs, provide a quick comparison between them?"
    # input_string = "InsecureRequestWarning: Unverified HTTPS request is being made to host"
    # input_string = "Compare mariadb and postgresql, when should I use them?"
    # input_string = "I have some servers that queries on a single mariadb, one of the server running on highload with high CPU and send a large number of queries to the database, and has very low query response time, but the others still has good response ime, what are the possibly root causes?"
    # input_string = "I have a small application with few tables and the amount of rows is not much, what type of database I should use? What kinds of problems likely to happened?"
    input_string = "I have a small application with few tables and the amount of rows is not much, what type of database I should use? What kinds of problems likely to happened? Please provide the specific database."
    # input_string = "My application have millions of records that also have high write/read frequency, what type of NoSQL I should use? Recommend me some NoSQL Database for this. I storing document data that are rarely change the structure."

    session_id = "this_is_session_id"

    start = time.time()
    res = main(input_string, session_id)
    # # res = prompt(input_string, type="parse")
    # print("-"*25 + f"RESULT in {round(time.time() - start)}s" + "-"*25)
    # print(res)







    # db = get_db()
    # for index, row in df_document.iterrows():
    #     db["documents"].insert_one({"prompt": input_string, "title": row["title"], "link": row["link"], "raw_document": row["raw_document"], "clean_document": row["clean_document"]})


    # documents = db["documents"]
    # res = find_by_id(documents, "6522e907666d033aa0ae07d2")
    # print(res)
