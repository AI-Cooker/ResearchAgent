from prompt_builder import prompt
from example_crawler import crawl
from db import get_db, find_by_id
import time

start = time.time()


input_string = "should I use capped collection or cluster-index collection in mongodb for storing user data?"
# 'cluster-index collection vs capped collection in mongodb',
# 'when to use capped collection vs cluster-index collection in mongodb',
# 'pros and cons of capped collection vs cluster-index collection in mongodb',
# 'which is better capped collection or cluster-index collection in mongodb for storing user data',
# 'which one should I use capped collection or cluster-index collection in mongodb for storing user data'


response = prompt(input=input_string, type="search")

df_document = None
for search_string in response:
    print(f"Crawling document for {search_string}")
    df_document = crawl(search_string=search_string, df_document=df_document)

clean_documents = []
for idx, raw_document in enumerate(df_document["raw_document"].tolist()):
    print(f"Cleaning document {idx}")
    clean_document = prompt(input=raw_document, type="clean")
    if clean_document:
        clean_documents.append(clean_document)
    else:
        # correct logic -> drop, but currently we need to improve the cleaner by examinating cannot processed docs
        # df_document.drop(idx)
        clean_documents.append("")

df_document["clean_document"] = clean_documents
print(df_document.head())

db = get_db()
for index, row in df_document.iterrows():
    db["documents"].insert_one({"prompt": input_string, "title": row["title"], "link": row["link"], "raw_document": row["raw_document"], "clean_document": row["clean_document"]})

print(f"Time: {time.time() - start}")

# documents = db["documents"]
# res = find_by_id(documents, "6522e907666d033aa0ae07d2")
# print(res)
