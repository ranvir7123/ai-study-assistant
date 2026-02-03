from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./study.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)
#each time used to make a new session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)