import chromadb

client = chromadb.Client()
collection = client.create_collection("research_agent")

def add_collections(dataset):
    collection.upsert(
        ids=dataset["links"],
        documents=dataset["documents"],
        metadatas=[{"title": title} for title in dataset["titles"]]
    )

def query_collections(input, n_result):
    res = collection.query(
        query_texts=input,
        n_results=min(n_result, collection.count()),
    )
    return res
