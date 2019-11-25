from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import part2
import datetime

engine = create_engine("mysql+mysqlconnector://yingzhi:123456@localhost/shipping", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def inventory(date):
    """
    date should be in the format "mm/nn/yyyy"
    """
    boats = session.query(part2.Reserves.bid, part2.Reserves.day)
    results = []
    for boat in boats:
        if boat.day == date:
            results.append({boat.bid: 0})
        else:
            results.append({boat.bid: 1})


def income(start, end):
    """
    Calculate business income during the period between two dates.
    :param start: start date of the period (include).
    :param end: end date of the period (include).
    :return: return a list payments of rent.
    """
    payments = session.query(part2.Reserves.bid). \
        select_from(part2.Reserves).all()
    print("*****")
    payments = session.query(part2.Sailors.name, part2.Payments.bid, part2.Payments.day, part2.Payments.payDay, part2.Payments.amount)#.\
        #select_from(part2.Payments)#. \
        #join(part2.Sailors, part2.Sailors.id == part2.Payments.sid)#. \
        #filter(part2.Payments.day >= start)#. \
        #filter(part2.Payments.day <= end)
    print("*****")
    results = []
    for payment in payments:
        results.append({"name": payment[0], "boat": payment[1], "rent_day": payment[2], "pay_day": payment[3], "amount": payment[4]})
    return results


if __name__ == "__main__":
    start = datetime.date(1998, 10, 10)
    end = datetime.date(1998, 10, 12)
    result = income(start, end)
    print(result)
