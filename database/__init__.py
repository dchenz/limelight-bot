from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

Base = declarative_base()
session_maker = sessionmaker()
Session = scoped_session(session_maker)
Base.query = Session.query_property()


def init_database(connection_string: str, debug: bool = False):
    """Create all tables defined by the model. Called after modules are imported."""
    engine = create_engine(connection_string, echo=debug)
    Session.remove()
    session_maker.configure(bind=engine)
    Base.metadata.create_all(bind=engine)

    if connection_string.startswith("sqlite:"):

        def _enable_fk(conn, _):
            conn.execute("PRAGMA foreign_keys=ON")

        event.listen(engine, "connect", _enable_fk)


DEFAULT_STRING_SIZE = 255
URL_STRING_SIZE = 2048
