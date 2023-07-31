from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def checkSession(id):
    # checkmadmin rights
    @wraps(id)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") > 1:
            return redirect("/")
        return id(*args, **kwargs)
    return decorated_function


def apology(massage):
    return render_template("apology.html", massage=massage, code="error403")



def init_month():
    month_list = []
    month = {}
    month["name"] = "Junuary"
    month["number"] = 1
    month_list.append(month)
    month = {}
    month["name"] = "Febrary"
    month["number"] = 2
    month_list.append(month)
    month = {}
    month["name"] = "March"
    month["number"] = 3
    month_list.append(month)
    month = {}
    month["name"] = "April"
    month["number"] = 4
    month_list.append(month)
    month = {}
    month["name"] = "May"
    month["number"] = 5
    month_list.append(month)
    month = {}
    month["name"] = "June"
    month["number"] = 6
    month_list.append(month)
    month = {}
    month["name"] = "July"
    month["number"] = 7
    month_list.append(month)
    month = {}
    month["name"] = "August"
    month["number"] = 8
    month_list.append(month)
    month = {}
    month["name"] = "September"
    month["number"] = 9
    month_list.append(month)
    month = {}
    month["name"] = "October"
    month["number"] = 10
    month_list.append(month)
    month = {}
    month["name"] = "November"
    month["number"] = 11
    month_list.append(month)
    month = {}
    month["name"] = "December"
    month["number"] = 12
    month_list.append(month)
    return month_list
