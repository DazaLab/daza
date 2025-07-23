import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

database_url = os.getenv("database_url")

engine = create_engine(
    database_url, 
    echo=False, #
    pool_size=10, #manter conexões simultaneas
    max_overflow=20, #quantidade de pessoas em espera
    pool_timeout=120, 
    pool_recycle=200
    )

SessinLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    return SessinLocal()