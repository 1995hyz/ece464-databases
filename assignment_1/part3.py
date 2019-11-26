from sqlalchemy import create_engine, and_, distinct
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


def get_income(start, end):
    """
    Calculate business income during the period between two dates.
    :param start: start date of the period (include).
    :param end: end date of the period (include).
    :return: return a list of payments of rent.
    """

    payments = session.query(part2.Sailors.name, part2.Payments.bid, part2.Payments.day, part2.Payments.payDay, part2.Payments.amount).\
        select_from(part2.Payments). \
        join(part2.Sailors, part2.Sailors.id == part2.Payments.sid). \
        filter(part2.Payments.day >= start). \
        filter(part2.Payments.day <= end). \
        all()
    results = []
    for payment in payments:
        results.append({"name": payment[0], "boat": payment[1], "rent_day": payment[2], "pay_day": payment[3], "amount": payment[4]})
    return results


def income_report_gen(start, end):
    """
    Print the income report.
    :param start: start date of the period (include).
    :param end: end date of the period (include).
    :return: None
    """
    payments = get_income(start, end)
    row_title = ["Name", "Boat", "Rent Day", "Pay Day", "Amount"]
    data = []
    for payment in payments:
        temp = []
        for title, value in payment.items():
            temp.append(str(value))
        data.append(temp)
    row_format = "{:>15}" * (len(row_title)+1)
    print(row_format.format("", *row_title))
    # for title, row in zip(row_title, data):
    total_income = 0
    for i in range(len(data)):
        print(row_format.format(i+1, *data[i]))
        total_income += int(data[i][4])
    print(row_format.format("SUM", *(["--------------"] * 4), str(total_income)))


def renter_accounting(sid, start, end):
    """
    Calculate a renter's all rent and payment activities during a period of time.
    :param sid: a renter's unique id.
    :param start: start date of the period (include).
    :param end: end date of the period (include).
    :return: return a list of debt that renters owe.
    """
    rents = session.query(distinct(part2.Sailors.name), part2.Reserves.bid, part2.Reserves.day, part2.Prices.price). \
        select_from(part2.Reserves). \
        join(part2.Prices, and_(part2.Reserves.sid == part2.Prices.sid, part2.Reserves.bid == part2.Prices.bid, part2.Reserves.day == part2.Prices.day)). \
        join(part2.Sailors, part2.Sailors.id == part2.Reserves.sid). \
        filter(part2.Sailors.id == sid). \
        filter(part2.Payments.day >= start). \
        filter(part2.Payments.day <= end). \
        all()
    payments = session.query(part2.Sailors.name, part2.Payments.bid, part2.Payments.payDay, part2.Payments.amount).\
        select_from(part2.Payments). \
        join(part2.Sailors, part2.Sailors.id == part2.Payments.sid). \
        filter(part2.Sailors.id == sid). \
        filter(part2.Payments.day >= start). \
        filter(part2.Payments.day <= end). \
        all()
    results = []
    for rent in rents:
        results.append({rent[2]: {"boat": rent[1], "credit": False, "amount": rent[3]}})
    for payment in payments:
        results.append({payment[2]: {"boat": payment[1], "credit": True, "amount": payment[3]}})
    results = sorted(results, key=lambda d: list(d.keys()))
    return [rents[0][0], results]


def renter_accounting_report_gen(sid, start, end):
    """
    Print a renter's accounting report.
    :param sid: a renter's unique id
    :param start: start date of the period (include).
    :param end: end date of the period (include).
    :return: None
    """
    results = renter_accounting(sid, start, end)
    print("Name: " + results[0])
    sum_value = 0
    row_title = ["Date", "Boat", "Rent", "Payment", "Sum"]
    row_format = "{:>15}" * len(row_title)
    print(row_format.format(*row_title))
    for result in results[1]:
        temp = list(result.keys()) + [value for key, value in list(result.values())[0].items()]
        if temp[2]:
            sum_value += temp[3]
            temp[2] = ""
        else:
            sum_value -= temp[3]
            temp[2] = temp[3]
            temp[3] = ""
        temp.append(sum_value)
        print(row_format.format(*[str(x) for x in temp]))
        

def get_debt(start, end):
    """
    Calculate debts that renters owe during a period of time.
    :param start: start date of the period (include).
    :param end: end date of the period (include).
    :return: return a list of debt that renters owe.
    """
    pass


if __name__ == "__main__":
    start_day = datetime.date(1998, 10, 10)
    end_day = datetime.date(1998, 11, 15)
    """
    result = income(start_day, end_day)
    print(result)
    """
    # income_report_gen(start_day, end_day)
    renter_accounting_report_gen(23, start_day, end_day)
