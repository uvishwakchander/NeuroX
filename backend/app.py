from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os

# -------------------------
# INIT
# -------------------------
app = FastAPI()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

# -------------------------
# MODELS
# -------------------------
class Message(BaseModel):
    text: str

class BurnoutInput(BaseModel):
    hours_worked: int
    tasks_done: int
    breaks_taken: int

class TaskInput(BaseModel):
    task: str

# -------------------------
# AI: COMMUNICATION COPILOT
# -------------------------
@app.post("/clarify")
def clarify_message(msg: Message):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""
            Rewrite the message below to be:
            - Clear
            - Kind
            - Professional
            - Neurodiversity-friendly
            - Low stress

            Message:
            {msg.text}
            """
        )
        return {"clarified": response.text}

    except Exception:
        return {
            "clarified": (
                "I’m feeling a bit overwhelmed right now. "
                "When you have time, I’d appreciate your support."
            )
        }

# -------------------------
# AI: BURNOUT DETECTION
# -------------------------
@app.post("/burnout")
def burnout_check(data: BurnoutInput):
    score = (data.hours_worked / (data.breaks_taken + 1)) - data.tasks_done

    if score >= 6:
        return {
            "status": "🚨 High burnout risk detected.",
            "suggestion": "Strongly recommend rest and workload reduction."
        }
    elif score >= 3:
        return {
            "status": "⚠️ Moderate load detected.",
            "suggestion": "Consider a short break or lighter task."
        }
    else:
        return {
            "status": "✅ Sustainable pace.",
            "suggestion": "Keep going gently 🌱"
        }

# -------------------------
# AI: QUEST GENERATOR
# -------------------------
@app.post("/quest")
def generate_quest(task: TaskInput):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""
            Convert this task into a gentle, motivating,
            neurodiversity-friendly quest with encouragement:

            Task: {task.task}
            """
        )

        return {
            "quest": response.text,
            "xp": 10,
            "rest_bonus": True
        }

    except Exception:
        return {
            "quest": f"🎯 {task.task} — take it one step at a time.",
            "xp": 10,
            "rest_bonus": True
        }

# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def root():
    return {"NeuroX": "Different Minds. Equal Power."}
