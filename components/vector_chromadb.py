import chromadb 

client = chromadb.HttpClient(host="localhost", port=8000)


def get_or_create_collection(name):
    return client.get_or_create_collection(name)


def check_already_in_db(problem, collection):
    results = collection.query(
        query_texts=problem,
        n_results=1)

    if results["ids"][0]:
        document = {
            "links": results["ids"][0],
            "documents": results["documents"][0],
            "titles": [item["title"] for item in results["metadatas"][0]]
        }
        return document, results["distances"][0][0]
    return None, None


def update_or_insert_to_collection(document, collection):
    collection.upsert(
        ids=document["links"],
        documents=document["documents"],
        metadatas=[{"title": title} for title in document["titles"]]
    )


def remove_collection(name):
    client.delete_collection(name)
