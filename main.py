from typing import Annotated
from fastapi import FastAPI, File, HTTPException, Depends, UploadFile
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import functions

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class CharacterBase(BaseModel):
    name: str
    strength: int 
    dexterity: int
    intelligence: int  
    wisdom: int
    vitality: int
    charisma: int
    agility: int
    lifePoints: int
    energyPoints: int
    image: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/api/upimage")
async def upload_images(file: UploadFile = File()) -> str:
    result = functions.upload_file(file, file.filename)
    if not result: 
        raise HTTPException(status_code=404, detail='NOT_FOUND')
    else: 
        return result

@app.post("/api/characters")
async def create_characters(character: CharacterBase, db: db_dependency):
    db_character = models.Character(name=character.name, 
                                    strength=character.strength, 
                                    dexterity=character.dexterity,
                                    intelligence=character.intelligence,
                                    wisdom=character.wisdom,
                                    vitality=character.vitality,
                                    charisma=character.charisma,
                                    agility=character.agility,
                                    lifePoints=character.lifePoints,
                                    energyPoints=character.energyPoints,
                                    image=character.image)
    
    db.add(db_character)
    db.commit()
    db.refresh(db_character)

@app.get("/api/characters")
async def search_characters(db: db_dependency, char_id: int | None = None):
    if char_id:
        result = db.get(models.Character, char_id)
        if not result:
            raise HTTPException(status_code=404, detail='NOT_FOUND')
        else:
            return result
    else: 
        result = db.query(models.Character).all()
        return result

@app.get("/api/roll")
async def roll_dice(roll_quantity: int = 1, face_count: int = 6, advantage: int = 0 ):
    if roll_quantity > 1000 or face_count > 1000 or advantage > 1000000:
        raise HTTPException(status_code=422, detail='TOO_BIG_NUMBERS_VALUES_EXCEED_LIMITS')
    else:
        result = functions.roll_dice(roll_quantity, face_count, advantage)
        return result