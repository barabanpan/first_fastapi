import databases
import sqlalchemy

from config import Config


metadata = sqlalchemy.MetaData()
database = databases.Database(
    Config.SQLALCHEMY_DATABASE_URI,
    force_rollback=True
)
