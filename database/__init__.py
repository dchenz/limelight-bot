import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

dotenv.load_dotenv()

_db_connection_string = os.environ.get("DISCORD_DB_STRING")
if _db_connection_string is None:
    print("Missing connection string (DISCORD_DB_STRING)")
    exit(1)

Base = declarative_base()

_engine = create_engine(_db_connection_string, echo=True)
Session = scoped_session(sessionmaker(bind=_engine))

Base.query = Session.query_property()


def init_database():
    """Create all tables defined by the model. Called after modules are imported."""

    Base.metadata.create_all(bind=_engine)
