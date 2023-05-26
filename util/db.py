import os
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes


def getconn():
    with Connector() as connector:
        conn = connector.connect(
            "testing-flask-api:asia-southeast2:flask-api-db-instance",  # Cloud SQL Instance Connection Name
            "pymysql",
            user="riski-db",
            password="riski123",
            db="flask_docker",
            ip_type=IPTypes.PUBLIC,  # IPTypes.PRIVATE for private IP
        )
        return conn


# engine_uri = "mysql+pymysql://{}:{}@{}:{}/{}".format(
#     os.environ["MYSQL_USER"],
#     os.environ["MYSQL_PASSWORD"],
#     os.environ["MYSQL_HOST"],
#     os.environ["MYSQL_PORT"],
#     os.environ["MYSQL_DB"],
# )

# db = SQLAlchemy()
