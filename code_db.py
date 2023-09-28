from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    name = Column(String, nullable=False)
    username = Column(String, unique=True, primary_key=True)
    password = Column(String, nullable=False)
    main_data = relationship('MainData')


class MainData(Base):
    __tablename__ = 'main_data'
    element_id = Column(Integer, primary_key=True, autoincrement=True)
    sugar_level = Column(String, nullable=True)
    fasting = Column(String, nullable=True)
    date = Column(String)
    time = Column(String)
    note = Column(String)
    username = Column(String, ForeignKey('user.username'))
    time_of_entry = Column(String)


if __name__ == "__main__":
    engine = create_engine('sqlite:///database/project_db.sqlite3')
    Base.metadata.create_all(engine)


# so database is created only if we run this file.