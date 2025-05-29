from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class Character(Base):
    __tablename__ = 'character'

    id = Column(Integer, primary_key= True, index= True, autoincrement= 'auto')
    name = Column(String, index= True, nullable= False)
    strength = Column(Integer, index = True, nullable= False)
    dexterity = Column(Integer, index = True, nullable= False)
    intelligence = Column(Integer, index = True, nullable= False)
    wisdom = Column(Integer, index = True, nullable= False)
    vitality = Column(Integer, index = True, nullable= False)
    charisma = Column(Integer, index = True, nullable= False)
    agility = Column(Integer, index = True, nullable= False)
    lifePoints = Column(Integer, index = True, nullable= False)
    energyPoints = Column(Integer, index = True, nullable= False)
    