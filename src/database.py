from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

DATABASE_FILE = "database.db"

sqlite_url = f"sqlite:///{DATABASE_FILE}"

connect_arcs = {"check_same_thread":False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_arcs)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as Session:
        yield Session
