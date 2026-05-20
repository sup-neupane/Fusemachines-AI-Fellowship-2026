from langchain_google_genai import ChatGoogleGenerativeAI  #type:ignore
from dotenv import load_dotenv  #type:ignore
from prompts.prompts import (
    SCHEMA_CONTEXT,
    DECOMPOSITION_PROMPT,
    SQL_GENERATION_PROMPT,
    SQL_FIX_PROMPT
)
import os

load_dotenv()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

def extract_text(response) -> str:
    """
    Safely extract text from LLM response.
    Handles both string and list responses.
    """
    content = response.content

    # If it's already a string
    if isinstance(content, str):
        return content

    # If it's a list of blocks
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                return block.get("text", "")
            if isinstance(block, str):
                return block
    return str(content)


def decompose_question(question: str) -> str:
    """
    Step 1: Break the natural language question
    into structured components using Gemini.
    """
    prompt = DECOMPOSITION_PROMPT.format(
        schema=SCHEMA_CONTEXT,
        question=question
    )
    response = llm.invoke(prompt)
    return extract_text(response)


def generate_sql(question: str, decomposition: str) -> str:
    """
    Step 2: Convert the structured decomposition
    into a SQL query using Gemini.
    """
    prompt = SQL_GENERATION_PROMPT.format(
        schema=SCHEMA_CONTEXT,
        decomposition=decomposition,
        question=question
    )
    response = llm.invoke(prompt)
    return extract_text(response)


def fix_sql(question: str, sql: str, error: str) -> str:
    """
    Step 3: Fix a failed SQL query using Gemini.
    Called only when execution fails (max 1 retry).
    """
    prompt = SQL_FIX_PROMPT.format(
        schema=SCHEMA_CONTEXT,
        sql=sql,
        error=error,
        question=question
    )
    response = llm.invoke(prompt)
    return extract_text(response)

def generate_summary(question: str, result: list) -> str:
    """
    Step 5: Convert SQL result into a natural language summary.
        """
    prompt = f"""
    You are a data analyst. Given a user question and the SQL query result, 
    write a single clear sentence summarizing the answer.

    Question: {question}
    Result: {result}

    Rules:
    - Write only one sentence
    - Be specific, include numbers if present
    - No markdown, no extra explanation
    """
    response = llm.invoke(prompt)
    return extract_text(response)


if __name__ == "__main__":
    question = "Get customer names and cities"

    print("=" * 50)
    print(f"Question: {question}")
    print("=" * 50)

    # Step 1: Decompose
    print("\n--- Decomposition ---")
    decomposition = decompose_question(question)
    print(decomposition)

    # Step 2: Generate SQL
    print("\n--- Generated SQL ---")
    sql = generate_sql(question, decomposition)
    print(sql)