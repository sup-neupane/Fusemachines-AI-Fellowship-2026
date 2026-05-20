from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END  #type:ignore
from sql_generator import decompose_question, generate_sql, fix_sql
from executor import execute_sql
from validator import clean_sql
from dotenv import load_dotenv  #type:ignore
from IPython.display import Image  #type:ignore

load_dotenv()

# ─── State Definition ────────────────────────────────────────────────────────
class PipelineState(TypedDict):
    question: str
    decomposition: str
    sql: str
    execution_result: dict
    retry_count: int
    status: str
    error: Optional[str]

# ─── Nodes ───────────────────────────────────────────────────────────────────

def decompose_node(state: PipelineState) -> PipelineState:
    """Node 1: Break question into structured components."""
    print(f"\n[INFO] Decomposing: {state['question']}")
    decomposition = decompose_question(state["question"])
    print(f"[INFO] Decomposition:\n{decomposition}")
    return {**state, "decomposition": decomposition}


def generate_sql_node(state: PipelineState) -> PipelineState:
    """Node 2: Generate SQL from decomposition."""
    print(f"\n[INFO] Generating SQL...")
    sql = generate_sql(state["question"], state["decomposition"])
    sql = clean_sql(sql)
    print(f"[INFO] Generated SQL:\n{sql}")
    return {**state, "sql": sql}


def execute_node(state: PipelineState) -> PipelineState:
    """Node 3: Execute SQL against PostgreSQL."""
    print(f"\n[INFO] Executing SQL...")
    result = execute_sql(
        state["sql"],
        state["question"],
        state["retry_count"]
    )
    print(f"[SUCCESS] Status: {result['status']}")
    if result["error"]:
        print(f"[ERROR] Error: {result['error']}")
    return {
        **state,
        "execution_result": result,
        "status": result["status"],
        "error": result["error"]
    }


def retry_node(state: PipelineState) -> PipelineState:
    """Node 4: Fix SQL and retry if execution failed."""
    print(f"\n[INFO] Retrying... Attempt {state['retry_count'] + 1}")
    fixed_sql = fix_sql(
        state["question"],
        state["sql"],
        state["error"]
    )
    fixed_sql = clean_sql(fixed_sql)
    print(f"[INFO] Fixed SQL:\n{fixed_sql}")
    return {
        **state,
        "sql": fixed_sql,
        "retry_count": state["retry_count"] + 1
    }


def output_node(state: PipelineState) -> PipelineState:
    """Node 5: Format and display final output."""
    result = state["execution_result"]
    print("\n" + "=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print(f"Question : {state['question']}")
    print(f"SQL      : {state['sql']}")
    print(f"Status   : {state['status']}")
    print(f"Retries  : {state['retry_count']}")
    if result.get("result"):
        print(f"Results  : {len(result['result'])} rows returned")
        for row in result["result"][:3]:
            print(f"  -> {row}")
    else:
        print(f"Error    : {state['error']}")
    print("=" * 60)
    return state


# ─── Conditional Edge ─────────────────────────────────────────────────────────

def check_execution(state: PipelineState) -> str:
    """
    Decide next step after execution:
    - If success → go to output
    - If failed and no retry yet → go to retry
    - If failed and already retried → go to output anyway
    """
    if state["status"] == "success":
        return "output"
    elif state["retry_count"] < 1:
        return "retry"
    else:
        print("\n[WARNING] Max retries reached. Moving to output.")
        return "output"


# ─── Build LangGraph ──────────────────────────────────────────────────────────

def build_pipeline():
    graph = StateGraph(PipelineState)

    # Add nodes
    graph.add_node("decompose", decompose_node)
    graph.add_node("generate_sql", generate_sql_node)
    graph.add_node("execute", execute_node)
    graph.add_node("retry", retry_node)
    graph.add_node("output", output_node)

    # Add edges
    graph.set_entry_point("decompose")
    graph.add_edge("decompose", "generate_sql")
    graph.add_edge("generate_sql", "execute")
    graph.add_edge("retry", "execute")
    graph.add_edge("output", END)

    # Conditional edge after execution
    graph.add_conditional_edges(
        "execute",
        check_execution,
        {
            "output": "output",
            "retry": "retry"
        }
    )

    return graph.compile()


# ─── Run Pipeline ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pipeline = build_pipeline()
    graph_image = pipeline.get_graph().draw_mermaid_png()
    with open("pipeline_graph.png", "wb") as f:
        f.write(graph_image)
        print(" Graph saved as pipeline_graph.png")

    # Test questions
    test_questions = [
        "List all products",
        "Get orders with customer names",
    ]

    for question in test_questions:
        initial_state = {
            "question": question,
            "decomposition": "",
            "sql": "",
            "execution_result": {},
            "retry_count": 0,
            "status": "",
            "error": None
        }
        pipeline.invoke(initial_state)
        print("\n")