from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqlconnector://yingzhi:123456@localhost/shipping", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Sailor(Base):
    __tablename__ = 'sailors'

    id = Column("sid", Integer, primary_key=True)
    name = Column("sname", String(30))
    rating = Column("rating", Integer)
    age = Column("age", Integer)


class Boats(Base):
    __tablename__ = 'boats'

    id = Column('bid', Integer, primary_key=True)
    name = Column("bname", String(20))
    color = Column("color", String(10))
    length = Column("length", Integer)


class Reserves(Base):
    __tablename__ = 'reserves'

    sid = Column('sid', Integer, primary_key=True)
    bid = Column('bid', Integer, primary_key=True)
    day = Column('day', Date, primary_key=True)


def question_1():
    sailors = session.query(Sailor).all()
    for sailor in sailors:
        print(sailor.name)


if __name__ == "__main__":
    question_1()
