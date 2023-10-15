import pprint
from google.generativeai.types.safety_types import HarmBlockThreshold
from google.generativeai.types.safety_types import HarmCategory
import google.generativeai as palm
import pandas as pd
import ast
from tenacity import retry, stop_after_attempt

palm.configure(api_key="AIzaSyBJKl57P-KrMx43TU4ojMtAO0qSoUWIjTs")

# parse_input_prompt = """You are an assistant that provides step by step for user to solve the problem in the user input.
# You need to figure out what the the main goal in the user input. Depend on the context in the user input, you need to provide step by step of the actions that user need to research for information on google.
# The response will follow as the format: ["what information need for action 1", "what information need for action 2"].
# Now I give you ther user input: '{}'"""

parse_input_prompt = ('You are an assistant that parses user input to several questions for searching on search engines: ["question 1", "question 2", "question 3", "question 4", ]. '
                      + 'When the user input is a complex problem, '
                      + 'you need to break it down into separate questions, focus on the special requirements from the user input if have. '
                      + 'The questions provided should contain the information from the user input. The maximum number of questions is 10.'
                      + 'The response will be a list contains all the questions string. '
                      + 'Here is the user input: "{}"')
                    #   + "Here are some examples: - user input: 'I have a large amount of queries on a single table with millions of record'")


query_string_prompt = """
You are an assistant that generates natural language queries for a Information Retrieval system based on user input. The queries should give information that related to the user input. The maximum number of search strings generated should be 5.
Think about what information you need to provide the correct answer for user input.
If the user input is a complex problem, you should break it down into easier parts.
Now help me generate queries for this: "{}"
"""


clean_prompt = """
You are an assistant that help user clean a raw document that may contains some nonsense words/characters. Please summarize as much detailed as possible.
When cleaning the document, you need to keep the information that related to this '{input_message}'.
Now I give you the document:
{document}
"""

# clean_prompt = """
# Summarize this document: 
# {document} 
# Focus on the information that related to '{input_message}'.
# """


analyze_prompt = """
You are an assistant that resolves the user input with the information in the given documents.
You need to analyze the information carefully for the question, then response in one of two option below:
1. If the given information is not enough to resolve the question, please response [INSUFFICIENT] and the reason. 
2. If the given information is enough, you must provide the detailed answer.
You MUST provide all the reference document links used at the end.
Here is the information:
{document_data}
And here is the user input: "{input_message}"
"""

defaults = {
    "model": "models/text-bison-001",
    "temperature": 0.2,
    # "candidate_count": 1,
    "top_k": 50,
    "top_p": 0.5,
    # "stop_sequences": [],
    "max_output_tokens": 2048,
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

defaults_chat = {
    "model": "models/chat-bison-001",
    "temperature": 0.1,
    "top_k": 35,
    "top_p": 0.1,
}

@retry(stop=stop_after_attempt(3))
def prompt(input: str, type: str, **kwargs):
    if type == "parse":
        final_prompt = parse_input_prompt.format(input)
        print(f"Number of tokens: {palm.count_message_tokens(prompt=final_prompt)}")
        completion = palm.generate_text(
            **defaults,
            prompt=final_prompt
        )
        if completion.result:
            print(completion.result)
            return ast.literal_eval(completion.result)
        else:
            print(f"{type.upper()} Sorry I cannot process your input: {completion}")
            return None
    elif type == "query":
        final_prompt = query_string_prompt.format(input)
        completion = palm.generate_text(
            **defaults,
            prompt=final_prompt,
        )
        if completion.result:
            print(completion.result)
        else:
            print(f"{type.upper()} Sorry I cannot process your input: {completion}")
            return None
    elif type == "clean":
        try:
            document = kwargs['document']
            print(f"Number of words: {len(document.split(' '))}")
            input_token_count = palm.count_message_tokens(prompt=f"{document} {input}")["token_count"]
            print(f"Number of tokens: {input_token_count}")
            if input_token_count > 8192 - 500 or input_token_count < 500:
                return None
            else:
                final_prompt = clean_prompt.format(input_message=input, document=document)
                completion = palm.generate_text(
                    **defaults,
                    prompt=final_prompt,
                )
                if completion.result:
                    return completion.result
                else:
                    print(f"{type.upper()} Sorry I cannot process your input: {completion}")
                    return None
        except Exception as exc:
            print(f"{type.upper()} An error happened during prompting: {exc}")
            return None
    elif type == "analyze":
        # try:
        data = kwargs['data']
        problems = kwargs['problems']
        document_data = ""
        for idx, problem in enumerate(problems):
            if data[problem]["documents"]:
                document_data += f"{idx}. {problem}\n"
                documents = data[problem]["documents"]
                titles = data[problem]["titles"]
                links = data[problem]["links"]
                for idx in range(len(titles)):
                    document_data += """
                    Document {idx}: Title: {title} - Link: {link}
                    Content: {content}
                    """.format(idx=idx+1, title=titles[idx], link=links[idx], content=documents[idx])
                    if palm.count_message_tokens(prompt=document_data)["token_count"] > 8192 - 500:
                        break
            document_data += "\n"
            
            
        final_prompt = analyze_prompt.format(document_data=document_data, input_message=input)
        print(f"Number of tokens: {palm.count_message_tokens(prompt=final_prompt)}")
        completion = palm.generate_text(
            **defaults,
            prompt=final_prompt,
        )
        if completion.result:
            return completion.result
        else:
            print(f"{type.upper()} Sorry I cannot process your input: {completion}")
            return None
        
        # response = palm.chat(
        #     **defaults_chat,
        #     context=document_data,
        #     messages=input,
        #     examples=[] 
        # )
        # if response.last:
        #     return response.last
        # else:
        #     print(f"{type.upper()} Sorry I cannot process your input: {response}")
        #     return None
        
        
        # except Exception as exc:
        #     print(f"{type.upper()} An error happened during prompting: {exc}")
        #     return None
        
        
        

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