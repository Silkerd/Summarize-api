from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

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

@app.get("/")
def read_root():
    return {"message": "API:t fungerar!"}

@app.post("/summarize")
async def summarize(req: SummaryRequest):
    try:
        client = OpenAI(api_key="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")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sammanfatta följande websida kortfattat."},
                {"role": "user", "content": req.text}
            ],
            temperature=0.5,
            max_tokens=150
        )

        summary = response.choices[0].message.content
        return JSONResponse(content={"summary": summary}, media_type="application/json; charset=utf-8")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, media_type="application/json; charset=utf-8")
