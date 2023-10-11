import pprint
from google.generativeai.types.safety_types import HarmBlockThreshold
from google.generativeai.types.safety_types import HarmCategory
import google.generativeai as palm
import pandas as pd
import ast

palm.configure(api_key="AIzaSyBJKl57P-KrMx43TU4ojMtAO0qSoUWIjTs")

parse_input_prompt = """
You are an assistant that parses the user input into a chain of thought.
If the user input was straight forward, you don't need to do anything.
Otherwise, you need to think about what information you would need to resolve the user input step by step.
The response will follow as the format: ["step 1", "step 2", "step 3", ].
Take a look at some examples:
- user input: When we need to use agile in software development?
- response: ["When we need to use agile in software development?"]
- user input: What are the currently best frameworks for web development, provide a comparison between them in term of difficulty in learning them.
- response: ["What are the currently best frameworks for web development", "Compare the difficulty in learning these web frameworks"]
Here is the user input: {}
"""

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
If the user input is a complex problem, you should break it down into easier parts.
Now help me generate queries for this: "{}"
"""

clean_prompt = """
You are an assistant that help user summarize a raw document that may contains some nonsense words/characters. Please summarize as much detailed as possible.
When summarizing the document, you need to keep the information that related to this {input_message}
Now I give you the document:
{document}
"""

synthesis_prompt = """
You are an assistant that help user synthesize the final document from given document parts. The as detailed as possible.
If there are dupplicates information between parts, you just keep one.
If there are nonsense lines that seems not related to the final document, you must remove it.
Now I give you all the document parts:
{}
"""


analyze_prompt = """
You are an assistant that resolves user input with the information in the given documents.
First, you need to read the information in the given documents carefully.
Then, you need to think what user would need in the response with the user input. If the user input is a complex problem, you should break it down into easier problems, and resolve one by one.
The response will be one from two cases:
1. If there is not enough information for resolving the user input, you must response "[INSUFFICIENT]" and the reason.
2. If there is enough information, you must provide the response from the given documents that might be the solution, and you need to provide the document Link to the information used.
Do not use any information outside the given documents.
Here are the documents:
{document_data}
And here is the user input: "{input_message}"
"""

defaults = {
    "model": "models/text-bison-001",
    # "temperature": 0.1,
    # "candidate_count": 1,
    # "top_k": 3000,
    # "top_p": 0.95,
    # "stop_sequences": [],
    "max_output_tokens": 8192,
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

def prompt(input: str, type: str, **kwargs):
    if type == "parse":
        final_prompt = parse_input_prompt.format(input)
        print(f"Number of tokens: {palm.count_message_tokens(prompt=final_prompt)}")
        completion = palm.generate_text(
            **defaults,
            prompt=final_prompt,
        )
        if completion.result:
            print(completion.result)
            return ast.literal_eval(completion.result)
        else:
            return "Sorry I cannot process your input"
    if type == "search":
        final_prompt = search_string_prompt.format(input)
        print(f"Number of tokens: {palm.count_message_tokens(prompt=final_prompt)}")
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
            document = kwargs['document']
            input_token_count = palm.count_message_tokens(prompt=f"{document} {input}")["token_count"]
            print(f"Number of tokens: {input_token_count}")
            if input_token_count > 8192 - 500:
                return None
                # Handle case when the document is too long
                # document_parts = []
                # start_idx = 0
                # while start_idx < len(input) - 2:
                #     cur_idx = start_idx + 1
                #     segment_length = palm.count_message_tokens(prompt=input[start_idx: cur_idx])["token_count"]
                #     while cur_idx < len(input) - 1 and segment_length < 8192 - 500:
                #         cur_idx += 1
                #         segment_length = palm.count_message_tokens(prompt=input[start_idx: cur_idx])["token_count"]
                #     if segment_length < 8192 - 500:
                #         completion = palm.generate_text(
                #             **defaults,
                #             prompt=clean_prompt.format(input[start_idx: cur_idx]),
                #         )
                #         if completion.result:
                #             document_parts.append(completion.result)
                #     start_idx = cur_idx + 1
                # if palm.count_message_tokens(prompt=document_parts)["token_count"] < 8192 - 500:
                #     completion = palm.generate_text(
                #         **defaults,
                #         prompt=clean_prompt.format(document_parts),
                #     )
                #     if completion.result:
                #         return completion.result
                #     else:
                #         print("Sorry I cannot process your input")
                #         return None      
                # else:
                #     idx = 1
                #     while idx < len(document_parts) - 1 and palm.count_message_tokens(prompt=document_parts[:idx])["token_count"] < 8192 - 500:
                #         idx += 1
                #     if idx > 1:
                #         completion = palm.generate_text(
                #             **defaults,
                #             prompt=clean_prompt.format(document_parts[:idx-1]),
                #         )
                #         if completion.result:
                #             return completion.result
                #         else:
                #             print("Sorry I cannot process your input")
                #             return None  
                #     else:
                #         print("Sorry I cannot process your input")
                #         return None  
            else:
                final_prompt = clean_prompt.format(input_message=input, document=document)
                completion = palm.generate_text(
                    **defaults,
                    prompt=final_prompt,
                )
                if completion.result:
                    return completion.result
                else:
                    print("Sorry I cannot process your input")
                    return None
        except Exception as exc:
            print(f"Sorry I cannot process your input. Error: {exc}")
            return None
    elif type == "analyze":
        try:
            document_content = kwargs['documents']
            titles = kwargs['titles']
            links = kwargs['links']
            document_data = ""
            for idx in range(len(titles)):
                document_data += """
                Document {idx}: {title}
                Link: {link}
                Content: {content}
                """.format(idx=idx+1, title=titles[idx], link=links[idx], content=document_content[idx])
                if palm.count_message_tokens(prompt=document_data)["token_count"] > 8192 - 500:
                    break
            final_prompt = analyze_prompt.format(document_data=document_data, input_message=input)
            print(f"Number of tokens: {palm.count_message_tokens(prompt=final_prompt)}")
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