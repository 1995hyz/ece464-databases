import pytest
import part2
from sqlalchemy import create_engine, Column, Integer, String, Date, func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqlconnector://yingzhi:123456@localhost/shipping", echo=True)

Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


def test_question_2():
    correct = {101: 2, 102: 3, 103: 3, 104: 5, 105: 3, 106: 3, 107: 1, 108: 1, 109: 4, 110: 3, 111: 1, 112: 1}
    boats = session.query(part2.Boats.id, func.count()).\
        join(part2.Reserves, part2.Boats.id == part2.Reserves.bid).\
        group_by(part2.Boats.id).\
        all()
    errors = []
    for boat in boats:
        if boat[0] not in correct:
            errors.append("Error: Unknown Boat with bid " + str(boat[0]) + " in database")
        elif boat[1] != correct[boat[0]]:
            errors.append("Error: Boat with bid " + str(boat[0]) + " miscount as " + str(boat[1]))
    assert not errors, "{}".format("\n".join(errors))


def test_question_3():
    correct = {22: "dusting", 23: "emilio", 24: "scruntus", 31: "lubber", 35: "figaro", 59: "stum", 61: "ossola",
               62: "shaun", 64: "horatio", 88: "dan", 89: "dye"}
    sailors = session.query(part2.Sailors.id, part2.Sailors.name).\
        select_from(part2.Reserves).\
        join(part2.Boats, part2.Boats.id == part2.Reserves.bid).\
        join(part2.Sailors, part2.Sailors.id == part2.Reserves.sid).\
        filter(part2.Boats.color == "red").\
        group_by(part2.Sailors.id).\
        all()
    errors = []
    for sailor in sailors:
        if sailor[0] not in correct:
            errors.append("Error: Unknown Sailor with sid " + str(sailor[0]) + " in database")
        elif sailor[1] != correct[sailor[0]]:
            errors.append("Error: Sailor with sid " + str(sailor[0]) + " has wrong name " + sailor[1])
    assert not errors, "{}".format("\n".join(errors))


def test_question_4():
    correct = {23: "emilio", 24: "scruntus", 35: "figaro", 61: "ossola", 62: "shaun"}
    not_red = session.query(part2.Sailors.id).\
        select_from(part2.Reserves).\
        join(part2.Boats, part2.Boats.id == part2.Reserves.bid).\
        join(part2.Sailors, part2.Sailors.id == part2.Reserves.sid).\
        filter(part2.Boats.color != "red").\
        group_by(part2.Sailors.id).\
        all()
    not_red_sailors = []
    for sailor in not_red:
        not_red_sailors.append(sailor.id)
    sailors = session.query(part2.Sailors.id, part2.Sailors.name).\
        select_from(part2.Reserves).\
        join(part2.Boats, part2.Boats.id == part2.Reserves.bid).\
        join(part2.Sailors, part2.Sailors.id == part2.Reserves.sid).\
        filter(part2.Boats.color == "red").\
        filter(part2.Sailors.id.notin_(not_red_sailors)).\
        all()
    errors = []
    for sailor in sailors:
        if sailor[0] not in correct:
            errors.append("Error: Unknown Sailor with sid " + str(sailor[0]) + " in database")
        elif sailor[1] != correct[sailor[0]]:
            errors.append("Error: Sailor with sid " + str(sailor[0]) + " has wrong name " + sailor[1])
    assert not errors, "{}".format("\n".join(errors))


def test_question_5():
    correct = {104: "Clipper"}
    max_reserve = session.query(part2.Boats.id, part2.Boats.name).\
        join(part2.Reserves, part2.Boats.id == part2.Reserves.bid).\
        group_by(part2.Boats.id).\
        order_by(desc(func.count())).\
        limit(1)
    assert max_reserve[0][0] == 104
    assert max_reserve[0][1] == "Clipper"


def test_question_6():
    correct = {60: "jit", 74: "horatio", 90: "vin"}
    sailors_red = session.query(part2.Sailors.id). \
        select_from(part2.Reserves). \
        join(part2.Boats, part2.Boats.id == part2.Reserves.bid). \
        join(part2.Sailors, part2.Sailors.id == part2.Reserves.sid). \
        filter(part2.Boats.color == "red"). \
        all()
    red_boat_sailors = []
    for sailor in sailors_red:
        red_boat_sailors.append(sailor.id)
    sailors = session.query(part2.Sailors.id, part2.Sailors.name).\
        select_from(part2.Reserves).\
        join(part2.Boats, part2.Boats.id == part2.Reserves.bid).\
        join(part2.Sailors, part2.Sailors.id == part2.Reserves.sid).\
        filter(part2.Sailors.id.notin_(red_boat_sailors)). \
        group_by(part2.Sailors.id). \
        all()
    errors = []
    for sailor in sailors:
        if sailor[0] not in correct:
            errors.append("Error: Unknown Sailor with sid " + str(sailor[0]) + " in database")
        elif sailor[1] != correct[sailor[0]]:
            errors.append("Error: Sailor with sid " + str(sailor[0]) + " has wrong name " + sailor[1])
    assert not errors, "{}".format("\n".join(errors))


def test_question_7():
    correct = 35
    average = session.query(func.avg(part2.Sailors.age)).filter(part2.Sailors.rating == 10)
    assert int(average[0][0]) == correct
