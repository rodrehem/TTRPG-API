import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DB_ENDPOINT = os.getenv('DB_ENDPOINT')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_PASS = os.getenv('DB_PASS')

URL_DATABASE = f'postgresql://{DB_USER}:{DB_PASS}@{DB_ENDPOINT}:5432/{DB_NAME}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()
