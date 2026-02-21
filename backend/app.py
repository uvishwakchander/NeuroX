from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/clarify")
def clarify_message(msg: Message):
    return {
        "clarified": f"Clear, kind version: {msg.text}"
    }

@app.get("/")
def root():
    return {"NeuroX": "Different Minds, Equal Power"}
