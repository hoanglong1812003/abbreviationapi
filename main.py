from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Abbreviation CRUD API")


# ===== Model =====
class Abbreviation(BaseModel):
    abbreviation: str
    meaning: str


class AbbreviationOut(Abbreviation):
    id: int


# ===== Fake Database (in-memory) =====
db = [
    {"id": 2, "abbreviation": "sd", "meaning": "sữa đặc"},
    {"id": 3, "abbreviation": "vnm", "meaning": "Vinamilk"},
    {"id": 4, "abbreviation": "sdd", "meaning": "sữa dinh dưỡng"},
    {"id": 8, "abbreviation": "sdn", "meaning": "sữa đậu nành"},
]


# ===== CRUD APIs =====

# READ ALL
@app.get("/abbreviations", response_model=list[AbbreviationOut])
def get_all():
    return db


# READ BY ID
@app.get("/abbreviations/{abbr_id}", response_model=AbbreviationOut)
def get_by_id(abbr_id: int):
    for item in db:
        if item["id"] == abbr_id:
            return item
    raise HTTPException(status_code=404, detail="Abbreviation not found")


# CREATE
@app.post("/abbreviations", response_model=AbbreviationOut)
def create_abbreviation(item: Abbreviation):
    new_id = max(i["id"] for i in db) + 1 if db else 1
    new_item = {
        "id": new_id,
        "abbreviation": item.abbreviation,
        "meaning": item.meaning,
    }
    db.append(new_item)
    return new_item


# UPDATE
@app.put("/abbreviations/{abbr_id}", response_model=AbbreviationOut)
def update_abbreviation(abbr_id: int, item: Abbreviation):
    for data in db:
        if data["id"] == abbr_id:
            data["abbreviation"] = item.abbreviation
            data["meaning"] = item.meaning
            return data
    raise HTTPException(status_code=404, detail="Abbreviation not found")


# DELETE
@app.delete("/abbreviations/{abbr_id}")
def delete_abbreviation(abbr_id: int):
    for i, data in enumerate(db):
        if data["id"] == abbr_id:
            db.pop(i)
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Abbreviation not found")
