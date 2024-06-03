from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_NAME, DB_ECHO_QUERY

engine = create_engine(f'sqlite:///{DB_NAME}', echo=DB_ECHO_QUERY)
Session = sessionmaker(bind=engine)
session = Session()
