import pprint
from google.generativeai.types.safety_types import HarmBlockThreshold
from google.generativeai.types.safety_types import HarmCategory
import google.generativeai as palm
import pandas as pd

palm.configure(api_key="AIzaSyBJKl57P-KrMx43TU4ojMtAO0qSoUWIjTs")

models = [
    m for m in palm.list_models() if "generateText" in m.supported_generation_methods
]
model = models[0].name
print(model)

prompt1 = """
You are an assistant that generates the search strings based on user input. The search strings are used for performing google search to find the information about the user input. You should think about all the possible questions that related to the user input which are related to risk, difficulties, pros and cons,... The maximum number of search strings generated should be 10.
Now help me generate search strings for this: "What is Retrieval Augmented Generation"
"""

prompt2 = """
You are an assistant that generates natural language queries for a Information Retrieval system based on user input. The queries should give information that related to the user input. The maximum number of search strings generated should be 10.
Now help me generate queries for this: "What is Retrieval Augmented Generation"
"""

defaults = {
    "model": "models/text-bison-001",
    "temperature": 0.1,
    # "candidate_count": 1,
    # "top_k": 3000,
    # "top_p": 0.95,
    # "stop_sequences": [],
    "max_output_tokens": 4096,
    "safety_settings": [
        {
            "category": HarmCategory.HARM_CATEGORY_DEROGATORY,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_TOXICITY,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_VIOLENCE,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_SEXUAL,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_MEDICAL,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_DANGEROUS,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
    ],
}


# completion = palm.generate_text(
#     model=model,
#     prompt=prompt1,
#     temperature=0,
#     # The maximum length of the response
#     max_output_tokens=2048,
# )
# print(completion.result)

# completion = palm.generate_text(
#     model=model,
#     prompt=prompt2,
#     temperature=0,
#     # The maximum length of the response
#     max_output_tokens=2048,
# )
# print(completion.result)


# completion = palm.generate_text(
#     **defaults,
#     prompt=prompt0,
# )

#  or the meaning of it does not related with the main context of the document, remove it.

# clean_prompt = """
# You are an assistant that help user remove nonsense or isolated words/characters in the given raw document and provide the cleaned document. With the rules below:
# - If you see a single line or a group of lines with few words/characters and not form a meaningful paragraph.
# - If you see some lines not in english and look like programming syntax, don't remove it.
# - Don't change or summarize anything about the document, keep all the original lines if it not be removed.
# Now I give you the document you need to clean:
# {}
# """

# You need to keep the most original words as much as possible in the raw document. You need to keep programming syntax if have.

clean_prompt = """
You are an assistant that help user summarize a raw document that may contains some nonsense words/characters. Please summarize as much detailed as possible.
Now I give you the document:
{}
"""

df_documents = pd.read_csv("components\\data\\documents\\rag.csv")
clean_documents = []

for idx, doc in enumerate(df_documents["raw_document"].tolist()):
    print(f"Processing file {idx}")
    final_prompt = clean_prompt.format(doc)
    # print(final_prompt)
    completion = palm.generate_text(
        **defaults,
        prompt=final_prompt,
    )
    # outputs = [output["output"] for output in completion.candidates]
    # for output in outputs:
    #     print(output)
    #     print("-" * 50)
    # print("-" * 50)
    # print(completion.result)
    if completion.result:
        clean_documents.append(completion.result)
    else:
        clean_documents.append("")
        print("Cannot summarize")

df_documents["clean_document"] = clean_documents

df_documents.to_csv("components\\data\\documents\\rag.csv")