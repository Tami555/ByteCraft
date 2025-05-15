import os
import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session


SqlAlchemyBase = orm.declarative_base()
__factory = None


def global_init():
    global __factory

    if __factory:
        return
    
    # SQLite
    connection_string = "sqlite:///db/computer_shop.db?check_same_thread=False"

    # SQL Server
    # connection_string = os.environ.get("SQL_SERVER_CONNECTION_STRING")
    # if not connection_string:
    #     driver_name = "ODBC Driver 17 for SQL Server"
    #     connection_string = f"mssql+pyodbc://DESKTOP-BHIDOQN/Computer_Shop?trusted_connection=yes&driver={driver_name}"

    try:
        engine = sqlalchemy.create_engine(connection_string, pool_size=10, max_overflow=20, echo=False)
        __factory = orm.sessionmaker(bind=engine)

        from . import __all_models

        SqlAlchemyBase.metadata.create_all(engine)

    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise

def create_session() -> Session:
    global __factory
    return __factory()