import pprint
from google.generativeai.types.safety_types import HarmBlockThreshold
from google.generativeai.types.safety_types import HarmCategory
import google.generativeai as palm
import pandas as pd
import ast

palm.configure(api_key="AIzaSyBJKl57P-KrMx43TU4ojMtAO0qSoUWIjTs")

search_string_prompt = """
You are an assistant that generates the search strings based on user input. The search strings are used for performing google search to find the information about the user input. You should think about all the possible questions that related to the user input which are related to risk, difficulties, pros and cons,... The maximum number of search strings generated should be 5.
The type of search strings shoud be relied on the type of the user input.
You shouldn't provide dupplicate search strings with the same meaning, think about unique ones.
You need to provide output as the following format: ['string 1', 'string 2', ].
Here are some examples:
- user input: "error: object reference not set to an instance of an object"
- response: ['What are the causes of the "error: object reference not set to an instance of an object?"', 'How to fix "object reference not set to an instance of an object?"']
- user input: "How to implement a RAG system?"
- response: ['what is a RAG system?', 'How to implement RAG system step by step?', 'What are the technoligies used for a RAG system?', 'What are the specials of a RAG system?', 'What are pros and cons of a RAG system?']
Now help me generate search strings for this: "{}"
"""

query_string_prompt = """
You are an assistant that generates natural language queries for a Information Retrieval system based on user input. The queries should give information that related to the user input. The maximum number of search strings generated should be 5.
Think about what information you need to provide the correct answer for user input.
If the user input is a complex, you should break it down into easier parts.
Now help me generate queries for this: "{}"
"""

clean_prompt = """
You are an assistant that help user summarize a raw document that may contains some nonsense words/characters. Please summarize as much detailed as possible.
Now I give you the document:
{}
"""

defaults = {
    "model": "models/text-bison-001",
    # "temperature": 0.1,
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

def prompt(input: str, type: str):
    if type == "search":
        final_prompt = search_string_prompt.format(input)
        completion = palm.generate_text(
            **defaults,
            prompt=final_prompt,
        )
        if completion.result:
            print(completion.result)
            return ast.literal_eval(completion.result)
        else:
            return "Sorry I cannot process your input"
    elif type == "query":
        final_prompt = query_string_prompt.format(input)
        completion = palm.generate_text(
            **defaults,
            prompt=final_prompt,
        )
        if completion.result:
            print(completion.result)
        else:
            print("Sorry I cannot process your input")
    elif type == "clean":
        try:
            final_prompt = clean_prompt.format(input)
            completion = palm.generate_text(
                **defaults,
                prompt=final_prompt,
            )
            if completion.result:
                return completion.result
            else:
                print("Sorry I cannot process your input")
                return None
        except:
            print("Sorry I cannot process your input")
            return None
        
        

# df_documents = pd.read_csv("components\\data\\documents\\rag.csv")
# clean_documents = []

# for idx, doc in enumerate(df_documents["raw_document"].tolist()):
#     print(f"Processing file {idx}")
#     final_prompt = clean_prompt.format(doc)
#     # print(final_prompt)
#     completion = palm.generate_text(
#         **defaults,
#         prompt=final_prompt,
#     )
#     # outputs = [output["output"] for output in completion.candidates]
#     # for output in outputs:
#     #     print(output)
#     #     print("-" * 50)
#     # print("-" * 50)
#     # print(completion.result)
#     if completion.result:
#         clean_documents.append(completion.result)
#     else:
#         clean_documents.append("")
#         print("Cannot summarize")

# df_documents["clean_document"] = clean_documents

# df_documents.to_csv("components\\data\\documents\\rag.csv")