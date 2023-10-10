from prompt_builder import prompt
from example_crawler import crawl
from db import get_db, find_by_id
from example_chroma import add_collections, query_collections
import time

start = time.time()


input_string = "What is lambda architecture?"

response = prompt(input=input_string, type="search")

df_document = None
for search_string in response[:1]: #For quick testing, just process the first search string 
    print(f"Crawling document for {search_string}")
    df_document = crawl(search_string=search_string, df_document=df_document, max_doc=5)

clean_documents = []
for idx, raw_document in enumerate(df_document["raw_document"].tolist()):
    print(f"Cleaning document {idx}")
    clean_document = prompt(input=raw_document, type="clean")
    print(f"CLEANED DOCUMENT: {clean_document}")
    if clean_document:
        clean_documents.append(clean_document)
    else:
        # correct logic -> drop, but currently we need to improve the cleaner by examinating cannot processed docs
        # df_document.drop(idx)
        clean_documents.append("")

df_document["clean_document"] = clean_documents
print(df_document.head())

dataset = {
    "documents": df_document["clean_document"].tolist(),
    "links": df_document["link"].tolist(),
    "titles": df_document["title"].tolist()
}

# Chromadb
add_collections(dataset)
chromadb_query = query_collections(input_string, n_result=10)
analyze_kwargs = {
    "documents": chromadb_query["documents"][0],
    "links": chromadb_query["ids"][0],
    "titles": [item["title"] for item in chromadb_query["metadatas"][0]],
}


result = prompt(input_string, type="analyze", **analyze_kwargs)

print(result)

# db = get_db()
# for index, row in df_document.iterrows():
#     db["documents"].insert_one({"prompt": input_string, "title": row["title"], "link": row["link"], "raw_document": row["raw_document"], "clean_document": row["clean_document"]})



print(f"Time: {time.time() - start}")

# documents = db["documents"]
# res = find_by_id(documents, "6522e907666d033aa0ae07d2")
# print(res)
