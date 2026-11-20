from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from sentence_transformers import SentenceTransformer

from boe_service.qdrant_db import connect_to_local, search
from boe_service.utils.json_utils import load_json

load_dotenv()
client = connect_to_local()
QUESTION_FILE_PATH = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "boe_service"
    / "evaluation"
    / "q_and_a.json"
)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

SYSTEM_PROMPT = """You are a chat agent that will answer user's query about the economy and policies.
You have access to tools that can retrieve information collected from Bank Of England's Monetary Policy and Minutes Meeting 
Ranging from Dates May 2022 to Sept 2026. You will read the retrieved text and decide what one is relevant and respond in a friendly manner. 
You will respond with information only found on the text and will tell the user if you cannot find any relevant information about their question."""


@tool
def retrieve_boe_information(query: str) -> list[dict] | str:
    """Calls a search function returning the top 5 paragraphs that has highest similarity
    score in vectors. The pool of documents stored are Bank of England's monetary policy summary
    from May 2022 - Sept 2026. The function will return the 5 paragraphs with their published date.
    The function will return error message string if retrival fail."""
    result = search(client, model, query, 5, False)
    if result is None or len(result) == 0:
        return "There is an unexpected failure in retrieving the text."
    retrieved_data = [
        {"published_date": i.payload["published_date"], "text": i.payload["text"]}
        for i in result
    ]
    return retrieved_data


agent = create_agent(
    "gpt-4o-mini",
    tools=[retrieve_boe_information],
    system_prompt=SYSTEM_PROMPT,
)


def inquire(question: str):
    response = agent.invoke({"messages": [HumanMessage(question)]})
    return response["messages"][-1].content


def main():
    q_and_a_data = load_json(QUESTION_FILE_PATH)

    llm_results = []

    for index, i in enumerate(q_and_a_data):
        question = i["question"]
        correct_answer = i["answer"]
        response = agent.invoke({"messages": [HumanMessage(question)]})
        llm_results.append([question, correct_answer, response["messages"][-1].content])
        print(f"{index + 1}/100 questions completed")

    result_df = pd.DataFrame(
        llm_results, columns=["question", "correct_answer", "answer"]
    )
    result_df.to_csv("agent_answers.csv", index=False)


if __name__ == "__main__":
    main()
