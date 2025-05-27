from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tillåt alla origins under utveckling, byt till din framer url i produktion
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummaryRequest(BaseModel):
    text: str
    detailed: bool = False

@app.get("/")
def read_root():
    return {"message": "API:t fungerar!"}

@app.post("/summarize")
async def summarize(req: SummaryRequest):
    try:

        if req.detailed:
            prompt = "Provide a detailed and thorough summary of the following website:"
        else:
            prompt = "Summarize the following website briefly:"

        max_tokens = 300 if req.detailed else 150
        
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": req.text}
            ],
            temperature=0.5,
            max_tokens=max_tokens
        )

        summary = response.choices[0].message.content
        return JSONResponse(content={"summary": summary}, media_type="application/json; charset=utf-8")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, media_type="application/json; charset=utf-8")
