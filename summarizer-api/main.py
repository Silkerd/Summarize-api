from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
import os

# Ladda API-nyckeln
load_dotenv()

app = FastAPI()

class SummaryRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "API:t fungerar!"}

@app.post("/summarize")
async def summarize(req: SummaryRequest):
    try:
        # Initiera klienten inuti funktionen
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

        summary = response.choices[0].message.content.encode("utf-8").decode("utf-8")
        return JSONResponse(content={"summary": summary}, media_type="application/json; charset=utf-8")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, media_type="application/json; charset=utf-8")
