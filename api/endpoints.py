from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anthropic import Anthropic
from conversations.manager import conversation_manager
import os

app = FastAPI()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic_client = Anthropic(api_key=anthropic_api_key)

class CodeInput(BaseModel):
    user_id: str
    prompt: str

@app.get("/api/sessions")
async def get_sessions():
    return conversation_manager.get_all_sessions()

@app.post("/api/sessions")
async def create_session():
    session_id = conversation_manager.create_new_session()
    return {"id": session_id}

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    context = conversation_manager.get_context(session_id)
    return {"conversation": context}

@app.post("/api/run-claude/")
async def run_claude(input: CodeInput):
    try:
        context = conversation_manager.get_context(input.user_id)
        context_text = "\n".join([f"User: {turn['user']}\nAI: {turn['ai']}" for turn in context])
        full_prompt = f"{context_text}\nUser: {input.prompt}\nAI:"

        if len(full_prompt.split()) > 100000:
            summary_response = anthropic_client.completions.create(
                model="claude-3-5-sonnet-20240620",
                prompt=f"Summarize the following conversation:\n\n{context_text}\n",
                max_tokens=150
            )
            summary = summary_response.choices[0].text.strip()
            conversation_manager.summarize_and_store(input.user_id)
            full_prompt = f"Summary:\n{summary}\nUser: {input.prompt}\nAI:"

        response = anthropic_client.completions.create(
            model="claude-3-5-sonnet-20240620",
            prompt=full_prompt,
            max_tokens=300
        )

        ai_response = response.choices[0].text.strip()
        conversation_manager.add_turn(input.user_id, input.prompt, ai_response)

        return {"response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))