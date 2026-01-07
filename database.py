from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///candidates.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    experience = Column(String)
    position = Column(String)
    location = Column(String)
    tech_stack = Column(String)
    questions = Column(String)

Base.metadata.create_all(engine)
