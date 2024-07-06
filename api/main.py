import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from anthropic import Anthropic, Completion

load_dotenv()

app = FastAPI()

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("Please set the ANTHROPIC_API_KEY environment variable")

anthropic_client = Anthropic(api_key=anthropic_api_key)

@app.post("/ai-assistant")
async def ai_assistant(prompt: str):
    try:
        response = anthropic_client.completions.create(
            model="claude-3-5-sonnet-20240620",
            prompt=prompt,
            max_tokens=300
        )
        return {"response": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))