from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from personal_info2 import sql_dialect_driver, username, password, host, database_name

def CreateConnection():
    db_url = f'{sql_dialect_driver}://{username}:{password}@{host}/{database_name}'
    engine = create_engine(db_url)
    Session = sessionmaker(engine)
    session = Session()
    Base = declarative_base()
    return engine, session, Base
