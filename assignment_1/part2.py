from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqlconnector://yingzhi:123456@localhost/shipping", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Sailors(Base):
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

    # For part3
    payments = relationship("Payments")


# For part3
class Payments(Base):
    __tablename__ = 'payments'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    sid = Column("sid", Integer, ForeignKey("Reserves.sid"))
    bid = Column("bid", Integer, ForeignKey("Reserves.bid"))
    day = Column("day", Date, ForeignKey("Reserves.day"))
    payDay = Column("payDay", Date)
    amount = Column("amount", Integer)


if __name__ == "__main__":
    pass
