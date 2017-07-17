from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('mysql+pymysql://root:TaylorHere357753@dab/escort?charset=utf8')
engine = create_engine('sqlite:///ziyuanbot.db',
                       convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
