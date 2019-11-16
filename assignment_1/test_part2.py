import pytest
import part2
from sqlalchemy import create_engine, Column, Integer, String, Date, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqlconnector://yingzhi:123456@localhost/shipping", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def test_question_2():
    correct = {101: 2, 102: 3, 103: 3, 104: 5, 105: 3, 106: 3, 107: 1, 108: 1, 109: 4, 110: 3, 111: 1, 112: 1}
    boats = session.query(part2.Boats.id, func.count()).join(part2.Reserves, part2.Boats.id == part2.Reserves.bid).group_by(part2.Boats.id).all()
    errors = []
    for boat in boats:
        if boat[0] not in correct:
            errors.append("Error: Unknown Boat with bid " + str(boat[0]) + " in database")
        elif boat[1] != correct[boat[0]]:
            errors.append("Error: Boat with bid " + str(boat[0]) + " miscount as " + str(boat[1]))
    assert not errors, "{}".format("\n".join(errors))


test_question_2()
