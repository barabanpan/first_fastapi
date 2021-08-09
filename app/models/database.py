import databases
import sqlalchemy

from .. import config


metadata = sqlalchemy.MetaData()
database = databases.Database(
    config.SQLALCHEMY_DATABASE_URI,
    force_rollback=True
)
