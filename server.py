import logging
import os

from dotenv import load_dotenv
from flask import Flask
from graphene import Schema
from graphql_server.flask import GraphQLView

from config import load_env_boolean, load_env_required
from database import init_database
from graphapi.queries.messages import MessagesQuery

load_dotenv()

if __name__ == "__main__":
    db_connection_string = load_env_required("DB_CONNECTION_STRING")

    logging.basicConfig(
        level=logging.getLevelName(os.environ.get("SERVER_LOG_LEVEL", "ERROR").upper()),
        format="%(asctime)s :: %(levelname)s :: %(message)s",
    )

    init_database(
        connection_string=db_connection_string,
        debug=load_env_boolean("SERVER_LOG_SQLALCHEMY"),
    )

    app = Flask(__name__)
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql", schema=Schema(MessagesQuery, auto_camelcase=False), graphiql=True
        ),
    )
    app.run(host="0.0.0.0", port=int(os.environ.get("SERVER_PORT", "5000")))
