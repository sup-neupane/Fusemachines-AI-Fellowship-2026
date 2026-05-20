from fastapi import FastAPI
from pydantic import BaseModel
from main import build_pipeline
from sql_generator import generate_summary

app = FastAPI(title="Mini SQL Agent", version="1.0")
pipeline = build_pipeline()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {"status": "running", "message": "Mini SQL Agent is live"}

@app.post("/agent/sql")
async def sql_agent(request: QuestionRequest):

    initial_state = {
        "question": request.question,
        "decomposition": "",
        "sql": "",
        "execution_result": {},
        "retry_count": 0,
        "status": "",
        "error": None
    }

    final_state = pipeline.invoke(initial_state)
    result = final_state["execution_result"].get("result", [])
    status = final_state["status"]

    # Generate summary only on success
    if status == "success":
        summary = generate_summary(request.question, result)
    else:
        summary = "Query failed after maximum retries."

    return {
        "sql": final_state["sql"],
        "result": result,
        "summary": summary,
        "status": status
    }