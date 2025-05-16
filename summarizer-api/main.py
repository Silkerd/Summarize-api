from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tillåt alla origins under utveckling
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
