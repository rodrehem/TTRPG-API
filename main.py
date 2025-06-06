from typing import Annotated, Optional
from fastapi import FastAPI, File, HTTPException, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import functions

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
    )

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

class CharacterUpdateBase(BaseModel):
    name: Optional[str] = None
    strength: Optional[int] = None
    dexterity: Optional[int] = None
    intelligence: Optional[int] = None  
    wisdom: Optional[int] = None
    vitality: Optional[int] = None
    charisma: Optional[int] = None
    agility: Optional[int] = None
    lifePoints: Optional[int] = None
    energyPoints: Optional[int] = None
    image: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

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

@app.post("/api/upimage")
async def upload_images(file: UploadFile = File()) -> str:
    result = functions.upload_file(file, file.filename)
    if not result: 
        raise HTTPException(status_code=404, detail='NOT_FOUND')
    else: 
        return result

@app.post("/api/characters", response_model = CharacterBase)
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
    return db_character

@app.patch("/api/characters", response_model = CharacterUpdateBase)
async def modify_characters(db: db_dependency, char_id: int, character: CharacterUpdateBase):
    db_character = db.get(models.Character, char_id)
    if not db_character:
        raise HTTPException(status_code=404, detail='NOT_FOUND')
    else:
        for key, value in character.model_dump(exclude_unset=True).items():
            print(db_character.name, key, value)
            setattr(db_character, key, value)
    
        db.add(db_character)
        db.commit()
        db.refresh(db_character)
        return db_character

@app.post("/api/roll")
async def roll_dice(roll_quantity: int = 1, face_count: int = 6, advantage: int = 0 ):
    if roll_quantity > 1000 or face_count > 1000 or advantage > 1000000:
        raise HTTPException(status_code=422, detail='TOO_BIG_NUMBERS_VALUES_EXCEED_LIMITS')
    else:
        result = functions.roll_dice(roll_quantity, face_count, advantage)
        return result