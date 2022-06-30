import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# from database.save import save_discord_message

dotenv.load_dotenv()

_db_connection_string = os.environ.get("DISCORD_DB_STRING")
if _db_connection_string is None:
    print("Missing connection string (DISCORD_DB_STRING)")
    exit(1)

debug_mode = os.environ.get("DEBUG")
if debug_mode is None:
    debug_mode = False
else:
    debug_mode = debug_mode.lower() in ("true", "1", "t")

Base = declarative_base()

_engine = create_engine(_db_connection_string, echo=debug_mode)
Session = scoped_session(sessionmaker(bind=_engine))

Base.query = Session.query_property()


def init_database():
    """Create all tables defined by the model. Called after modules are imported."""

    Base.metadata.create_all(bind=_engine)
