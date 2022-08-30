import re
import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

FOUL_WORD_LIST = [
    "foul1",
    "foul2",
    "foul3",
    "foul4",
    "foul5",
    "foul6",
]


class Sentence(BaseModel):
    fragment: str


app = FastAPI()


@app.post("/sentences/")
async def check_moderation(sentence: Sentence):
    service_available = random.choice([1, 1, 1, 0])
    if not service_available:
        raise HTTPException(status_code=503, detail="Service unavailable")
    has_foul_language = False
    for word in FOUL_WORD_LIST:
        foul_word_re = re.compile(re.escape(word), re.IGNORECASE)
        if foul_word_re.search(sentence.fragment):
            has_foul_language = True
            break

    return {"has_foul_language": has_foul_language}
