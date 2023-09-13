# ResearchAgent

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![ElasticSearch](https://img.shields.io/badge/-ElasticSearch-005571?style=for-the-badge&logo=elasticsearch)
![Google](https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white)


An LLM-powered agent that able to explore and analyze information in the internet for a specific topic.

To do:
- [ ] Setup project structure.
- [ ] Choose technology stack.
- [ ] Add documents.
- [ ] Define milestones and task list.
- [ ] ...

## Main Workflow and Components

![Workflow](https://media.discordapp.net/attachments/1138374774268104718/1148872832491737118/Diagram_1.jpg?width=792&height=452)

## Technology Stack

- **Large Language Model**: For easier development, we use open-access LLMs like LLaMA 2 or Falcon API instead of the ChatGPT API. However, during development, we should define a metric to compare these LLMs. And we will use Langchain to wrap up the prompting process.
- **Vector Store/Vector Database/Retriever**: There are many options like ChromaDB or FAISS (more information at https://python.langchain.com/docs/modules/data_connection/). We need a real test for the performance of these approaches in case of our requirements.
- **Crawler**: Currently, we just use Python packages to do this because of the huge customizations needed in the Agent. If we have time, we can investigate a third-party crawler if it fits our requirements.
- **Parser**:
  - **The HTML parser/cleaner**: We need to find a general way to clean up HTML tags and remove the unused parts in retrieved HTML (e.g., keep the innerText of p and h tags only). BeautifulSoup might be enough for this.
  - **The context parser**: In most cases, we can't store all the cleaned data directly in the storage; we need to split it into smaller documents with complete meanings and as small as possible. Langchain supports some text splitters, but it might not be enough. We can use some deep learning approaches to overcome this, like sentence similarity.
- **Webserver**: A simple web application framework like Flask or FastAPI may be enough for this. We just need a simple REST API.
- **Hosting and Deploying**: We don't host any ML models, so free and simple cloud hosting like https://dashboard.render.com/ is enough.


