from fastapi import FastAPI
from pydantic import BaseModel
from app.retriever import retrieve_chunks
from app.memory import get_history, push_turn
from app.prompt import build_prompt
from app.chat_engine import chat_completion

app = FastAPI()

class ChatRequest(BaseModel):
    session: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    hits = retrieve_chunks(req.message)
    history = get_history(req.session)
    prompt = build_prompt(req.message, hits, history)
    answer = chat_completion(prompt)
    push_turn(req.session, "user", req.message)
    push_turn(req.session, "assistant", answer)
    return {"answer": answer, "sources": hits}
 
