from torch import cuda
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import os
import pinecone
import time

os.environ["REQUESTS_CA_BUNDLE"] = "D:\\Storages\\certs\\tma-ADCA-CA.crt"
os.environ["CURL_CA_BUNDLE"] = "D:\\Storages\\certs\\tma-ADCA-CA.crt"

embed_model_id = "sentence-transformers/all-MiniLM-L6-v2"

device = f"cuda:{cuda.current_device()}" if cuda.is_available() else "cpu"

embed_model = HuggingFaceEmbeddings(
    model_name=embed_model_id,
    model_kwargs={"device": device},
    encode_kwargs={"device": device, "batch_size": 32},
)

docs = ["this is one document", "and another document"]

embeddings = embed_model.embed_documents(docs)

print(
    f"We have {len(embeddings)} doc embeddings, each with "
    f"a dimensionality of {len(embeddings[0])}."
)

pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY")
    or "b2c61a1e-ed0c-495d-b5f5-eb8e8babdb01",
    environment=os.environ.get("PINECONE_ENVIRONMENT") or "gcp-starter",
)


index_name = "palm-rag"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=len(embeddings[0]), metric="cosine")
    # wait for index to finish initialization
    while not pinecone.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pinecone.Index(index_name)
index.describe_index_stats()

# batch_size = 32

# for i in range(0, len(data), batch_size):
ids = [f"rag-{i}" for i in range(45)]
texts = []
file_format = "document_{}.txt"
for i in range(45):
    file_name = file_format.format(i)
    with open(
        f"components\\data\\cleaned_documents\\retrieval_augmented_generation\\{file_name}",
        "r",
    ) as finput:
        texts.append(finput.read())
embeds = embed_model.embed_documents(texts)
# get metadata to store in Pinecone
metadata = [f"document-{i}" for i in range(45)]
# add to Pinecone
index.upsert(vectors=zip(ids, embeds, metadata))

index.describe_index_stats()

text_field = "text"  # field in metadata that contains text content

vectorstore = Pinecone(index, embed_model.embed_query, text_field)


query = "what makes RAG special?"

vectorstore.similarity_search(
    query, k=3  # the search query  # returns top 3 most relevant chunks of text
)
