import os
from flask_sqlalchemy import SQLAlchemy

engine_uri = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    os.environ["MYSQL_USER"],
    os.environ["MYSQL_PASSWORD"],
    os.environ["MYSQL_HOST"],
    os.environ["MYSQL_PORT"],
    os.environ["MYSQL_DB"],
)

db = SQLAlchemy()
