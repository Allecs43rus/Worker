from flask import Flask, render_template, redirect, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from calendar import monthrange, Calendar



from helpers import login_required, apology, init_month, checkSession


app = Flask(__name__)

DAYS = 0


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# database
db = SQL("sqlite:///worker.db")


@app.route("/")
@login_required
def hello():
    months = init_month()
    yearNow = datetime.now().year
    monthNow = datetime.now().month
    date = str(monthNow) + "." + str(yearNow)
    days = monthrange(yearNow, monthNow)[1]

    # create dictionary with current date
    for month in months:
        if month["number"] == monthNow:
            now = {}
            now["year"] = yearNow
            now["month"] = month["name"]
    if request.method == "GET":

        # create new list with dictionary
        try:
            info = db.execute("SELECT number, name, day, shift, position  FROM users JOIN ? ON ?.id_user = users.id;", date, date)
            if len(info) == 0:
                return redirect("/new")
            shifts = []
            print(info)
            while True:
                if len(shifts) == 0:
                    shift = {}
                    shift["name"] = info[0]["name"]
                    shift["number"] = info[0]["number"]
                    shift["position"] = info[0]["position"]
                    shift[info[0]["day"]] = info[0]["shift"]
                    shifts.append(shift)
                else:
                    for data in info:
                        counter = 0
                        for shift in shifts:
                            if shift["name"] == data["name"]:
                                shift[data["day"]] = data["shift"]
                                break
                            counter += 1
                        if counter == len(shifts):
                            shift = {}
                            shift["number"] = data["number"]
                            shift["name"] = data["name"]
                            shift["position"] = data["position"]
                            shift[data["day"]] = data["shift"]
                            shifts.append(shift)
                    break
        except RuntimeError:
            return redirect("/new")
        return render_template("index.html", now=now, days=days, shifts=shifts)
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    name = request.form.get("username")
    password = request.form.get("password")

    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST" and name and password:
        nameDB = db.execute("SELECT username FROM users WHERE username = ?;", name)
        passwordDB = db.execute ("SELECT hash FROM users WHERE username = ?", name)
        userID = db.execute("SELECT id FROM users WHERE username = ?;", name)
        if len(nameDB) == 1 and len(passwordDB) == 1 and check_password_hash(passwordDB[0]["hash"], password ):
            session["user_id"] = userID[0]["id"]
            return redirect("/")
        else:
            return apology("please insert correct name or password")
    else:
        return apology("wtf")
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/registr", methods=["GET", "POST"])
@login_required
@checkSession
def registration():
    if request.method == "GET":
        employees = db.execute("SELECT * FROM users")
        rows = []
        for employee in employees:
            row = {}
            row["num"] = employee['id']
            row["name"] = employee['username']
            row["password"] = employee['password']
            row["position"] = employee['position']
            rows.append(row)
        return render_template("registr.html", rows=rows)
    elif request.method == "POST":
        if request.form.get("choose") == "new" and request.form.get("surname") and request.form.get("name") and request.form.get("password") and request.form.get("position"):
            name = request.form.get("surname") + " " + request.form.get("name")
            password = request.form.get("password")
            hash = generate_password_hash(password)
            position = request.form.get("position")
            db.execute("INSERT INTO users(username, hash, position, password) VALUES (?, ?, ?, ?);", name, hash, position, password)
            return redirect("/registr")
        elif request.form.get("choose") == "delete" and request.form.get("surname") and request.form.get("name") and request.form.get("sure") == "ok":
            name = request.form.get("surname") + " " + request.form.get("name")
            if name != "BOSS" and db.execute("SELECT * FROM users WHERE username =?;", name):
                db.execute("DELETE FROM users WHERE username = ?;", name)
                return redirect("/registr")
            else:
                return apology("No such user")

        else:
            return apology("Please, fill in all the fields ")
        

@app.route("/new", methods=["GET", "POST"])
@login_required
@checkSession
def new_shedule():
    months = init_month()
    if request.method == "GET":
        year = datetime.now().year
        return render_template("new.html", months=months, year=year)
    elif request.method == "POST":
        if request.form.get("year") and request.form.get("month"):
            month = request.form.get("month")
            year = request.form.get("year")
            days = monthrange(int(year), int(month))[1]
            peoples = db.execute("SELECT username, position FROM users;")
            for dict in months:
                if dict["number"] == int(month):
                    nameMonth = dict["name"]
            return render_template("new.html", days=days, nameMonth=nameMonth, peoples=peoples, year=year, month=month)
        elif request.form.get("1"): 
            days = request.form.get("days")
            year = request.form.get("yearInput")
            month = request.form.get("monthInput")
            countPeople = db.execute("SELECT COUNT(id) FROM users;")[0]["COUNT(id)"]
            shifts = []
            for count in range(1, countPeople + 1):
                for n in range(1, int(days) + 1):
                    shift = {}
                    shift["number"] = count
                    shift["year"] = int(year)
                    shift["month"] = int(month)
                    shift["day"] = n
                    shift["name"] = request.form.get(str(count))
                    shift["shift"] = request.form.get("№" + str(count) + "date" + str(n))
                    shifts.append(shift)
            date = month + "." + year
            if db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?", date):
                db.execute("DROP TABLE ?;", date)
                db.execute("CREATE TABLE ? (id_user INTEGER NOT NULL, number INTEGER, year INTEGER, month INTEGER, day INTEGER, name TEXT, shift TEXT);", date)
            else:
                db.execute("CREATE TABLE ? (id_user INTEGER NOT NULL, number INTEGER, year INTEGER, month INTEGER, day INTEGER, name TEXT, shift TEXT);", date)
            for shift in shifts:
                id = db.execute("SELECT id FROM users WHERE username = ?;", shift["name"])
                if id:
                    db.execute("INSERT INTO ? (id_user, number, year, month, day, name, shift) VALUES (?, ?, ?, ?, ?, ?, ?);", date, id[0]["id"], shift["number"], shift["year"], shift["month"], shift["day"], shift["name"], shift["shift"])
            return redirect("/")   
        else:
            return apology("Please, insert data")
        

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit_shedule():
    months = init_month()
    yearNow = datetime.now().year
    monthNow = datetime.now().month
    date = str(monthNow) + "." + str(yearNow)
    days = monthrange(yearNow, monthNow)[1]

    # current and next month
    for month in months:
        if month["number"] == monthNow:
            now = {}
            now["year"] = yearNow
            now["month"] = month["name"]
            now["monthNumber"] = month["number"]
            now["days"] = days
        if month["number"] == monthNow + 1 and db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?", str(monthNow + 1) + "." + str(yearNow)):
            now["nextMonthNumber"] = month["number"]
            now["nextMonth"] = month["name"]
            now["nextYear"] = yearNow
            now["daysNextMonth"] = monthrange(yearNow, monthNow + 1)[1]
        elif month["number"] == monthNow and monthNow == 12 and db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?", str(1) + "." + str(yearNow + 1)):
            now["nextMonthNumber"] = 1
            now["nextMonth"] = "Jenuary"
            now["nextYear"] = yearNow + 1
            now["daysNextMonth"] = monthrange(yearNow + 1, 1)[1]

    if request.method == "GET":
        if db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?", date):
            # shedule current month
            try:
                info = db.execute("SELECT number, name, day, shift, position  FROM users JOIN ? ON ?.id_user = users.id;", date, date)
                if not info:
                    return redirect("/new")
                shifts = []
                while True:
                    if len(shifts) == 0:
                        shift = {}
                        shift["name"] = info[0]["name"]
                        shift["number"] = info[0]["number"]
                        shift["position"] = info[0]["position"]
                        shift[info[0]["day"]] = info[0]["shift"]
                        shifts.append(shift)
                    else:
                        for data in info:
                            counter = 0
                            for shift in shifts:
                                if shift["name"] == data["name"]:
                                    shift[data["day"]] = data["shift"]
                                    break
                                counter += 1
                            if counter == len(shifts):
                                shift = {}
                                shift["number"] = data["number"]
                                shift["name"] = data["name"]
                                shift["position"] = data["position"]
                                shift[data["day"]] = data["shift"]
                                shifts.append(shift)
                        break
            except RuntimeError:
                return redirect("/new")
            # shedule next month
            try:
                info = db.execute("SELECT number, name, day, shift, position  FROM users JOIN ? ON ?.id_user = users.id;", str(now["nextMonthNumber"]) + "." + str(now["nextYear"]), str(now["nextMonthNumber"]) + "." + str(now["nextYear"]))
                if not info:
                    return render_template("edit.html", now=now, shifts=shifts)
                shiftsNext = []
                while True:
                    if len(shiftsNext) == 0:
                        shift = {}
                        shift["name"] = info[0]["name"]
                        shift["number"] = info[0]["number"]
                        shift["position"] = info[0]["position"]
                        shift[info[0]["day"]] = info[0]["shift"]
                        shiftsNext.append(shift)
                    else:
                        for data in info:
                            counter = 0
                            for shift in shiftsNext:
                                if shift["name"] == data["name"]:
                                    shift[data["day"]] = data["shift"]
                                    break
                                counter += 1
                            if counter == len(shiftsNext):
                                shift = {}
                                shift["number"] = data["number"]
                                shift["name"] = data["name"]
                                shift["position"] = data["position"]
                                shift[data["day"]] = data["shift"]
                                shiftsNext.append(shift)
                        break
                return render_template("edit.html", now=now, shifts=shifts, shiftsNext=shiftsNext)
            except KeyError:
                return render_template("edit.html", now=now, shifts=shifts)
        else:
            return render_template("new.html")        
    if request.method == "POST":
        days = request.form.get("days")
        year = request.form.get("yearInput")
        month = request.form.get("monthInput")
        countPeople = db.execute("SELECT COUNT(id) FROM users;")[0]["COUNT(id)"]
        shifts = []
        for count in range(1, countPeople + 1):
            for n in range(1, int(days) + 1):
                shift = {}
                shift["number"] = count
                shift["year"] = int(year)
                shift["month"] = int(month)
                shift["day"] = n
                shift["name"] = request.form.get(str(count))
                shift["shift"] = request.form.get("№" + str(count) + "date" + str(n))
                shifts.append(shift)
        date = month + "." + year
        for shift in shifts:
            db.execute("UPDATE ? SET shift = ? WHERE name = ? AND day = ?;", date, shift["shift"], shift["name"], shift["day"])
        return redirect("/")
                

@app.route("/my_shifts", methods=["GET", "POST"])
@login_required
def my_shifts(): 
    months = init_month()
    yearNow = datetime.now().year
    monthNow = datetime.now().month
    dateNow ={}
    dateNow["year"] = yearNow
    dateNow["monthNumber"] = monthNow
    cal = Calendar()
    daysCalendar = cal.monthdays2calendar(yearNow, monthNow)

    datas = []
    for n in range(1, 13):
        if db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?", str(n) + "." + str(yearNow)):       
            data = {}
            data["yearNow"] = yearNow
            data["number"] = n
            for month in months:
                if month["number"] == monthNow:
                    dateNow["monthName"] = month["name"]
                if month["number"] == n:
                    data["nameMonth"] = month["name"]
            datas.append(data)
        if db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?", str(n) + "." + str(yearNow + 1)):       
            data = {}
            data["yearNext"] = yearNow + 1
            data["number"] = n
            for month in months:
                if month["number"] == n:
                    data["nameMonth"] = month["name"]
            datas.append(data)
            
    if request.method == "GET":
        date = str(monthNow) + "." + str(yearNow)
        myShifts = db.execute("SELECT day, shift FROM ? WHERE id_user = ?;", date, session["user_id"])

        shifts = {}
        shifts["inspector"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", date, session["user_id"], "inspector")[0]["COUNT(shift)"]
        shifts["driver"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", date, session["user_id"], "driver")[0]["COUNT(shift)"]
        shifts["major"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", date, session["user_id"], "major")[0]["COUNT(shift)"]
        shifts["majorDriver"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", date, session["user_id"], "majorDriver")[0]["COUNT(shift)"]

        total = {}
        total["shifts"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift != ?;", date, session["user_id"], "dayOff")[0]["COUNT(shift)"]
        total["dayOff"] = monthrange(yearNow, monthNow)[1] - total["shifts"]
        costShifts = db.execute("SELECT * FROM cost;")
        total["money"] = 0
        for shift in costShifts:
            if shift["shift_name"] in shifts:
                total["money"] += shift["cost"] * shifts[shift["shift_name"]]
        return render_template("my_shifts.html", datas=datas, dateNow=dateNow, daysCalendar=daysCalendar, myShifts=myShifts, shifts=shifts, total=total)
    
    if request.method == "POST":
        queryMonth = request.form.get("month")
        queryYear = request.form.get("year")
        dateNow["monthNumber"] = int(queryMonth)
        dateNow["year"] = int(queryYear)
        data["yearNext"] = yearNow
        for month in months:
            if month["number"] == dateNow["monthNumber"]:
                dateNow["monthName"] = month["name"]
        requestDate = queryMonth + "." + queryYear
        if db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?;", requestDate):
            myShifts = db.execute("SELECT day, shift FROM ? WHERE id_user = ?;", requestDate, session["user_id"])

            shifts = {}
            shifts["inspector"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", requestDate, session["user_id"], "inspector")[0]["COUNT(shift)"]
            shifts["driver"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", requestDate, session["user_id"], "driver")[0]["COUNT(shift)"]
            shifts["major"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", requestDate, session["user_id"], "major")[0]["COUNT(shift)"]
            shifts["majorDriver"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift = ?;", requestDate, session["user_id"], "majorDriver")[0]["COUNT(shift)"]

            total = {}
            total["shifts"] = db.execute("SELECT COUNT(shift) FROM ? WHERE id_user = ? AND shift != ?;", requestDate, session["user_id"], "dayOff")[0]["COUNT(shift)"]
            total["dayOff"] = monthrange(yearNow, monthNow)[1] - total["shifts"]
            costShifts = db.execute("SELECT * FROM cost;")
            total["money"] = 0
            for shift in costShifts:
                if shift["shift_name"] in shifts:
                    total["money"] += shift["cost"] * shifts[shift["shift_name"]]

            return render_template("my_shifts.html", datas=datas, dateNow=dateNow, daysCalendar=daysCalendar, myShifts=myShifts, shifts=shifts,total=total)
        else:
            return apology("Please insert correct date")
        

@app.route("/cost", methods=["GET", "POST"])
@login_required
@checkSession
def cost():
    shiftCost = db.execute("SELECT * FROM cost")
    if request.method == "GET":
        return render_template("cost.html",shiftCost=shiftCost)
    elif request.method == "POST":
        for dict in shiftCost:
            if request.form.get(dict["shift_name"]):
                db.execute("UPDATE cost SET cost = ? WHERE shift_name = ?;", int(request.form.get(dict["shift_name"])), dict["shift_name"])
                return redirect("/cost")
            else:
                return redirect("/cost")
            

@app.route("/calculations", methods=["GET"])
@login_required
@checkSession
def bookeeper():
    months = init_month()
    dateReport ={}
    if datetime.now().month == 1:
        dateReport["monthNumber"] == 12
        dateReport["year"] = datetime.now().year - 1
    else:
        dateReport["monthNumber"] = datetime.now().month - 1
        dateReport["year"] = datetime.now().year
    for month in months:
        if month["number"] == dateReport["monthNumber"]:
            dateReport["name"] = month["name"]
        date = str(dateReport["monthNumber"]) + "." + str(dateReport["year"])

    if request.method == "GET" and db.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name = ?", date):
        info = db.execute("SELECT name, shift_name, cost FROM ? JOIN cost ON ?.shift = cost.shift_name;", date, date)
        workers = db.execute("SELECT name FROM ? GROUP BY name;", date)
        shifts = db.execute("SELECT * FROM cost;")
        cost = {}
        for shift in shifts:
            cost[shift["shift_name"]] = shift["cost"]
        listDatas =[]
        for worker in workers:
            data = {}
            data["name"] = worker["name"]
            listDatas.append(data)
        for every in info:
            for data in listDatas:
                if every["name"] == data["name"]:
                    if every["shift_name"] in data:
                        data[every["shift_name"]] += 1
                    else:
                        data[every["shift_name"]] = 1
        listDatas = [data for data in listDatas if len(data) > 1]
        keysCost = list(cost.keys())
        totalCalc = 0
        for data in listDatas:
            data["positions"] = len(data) - 1
            data["totalMoney"] = 0
            for key in keysCost:
                if key in data:
                    data["totalMoney"] += cost[key] * data[key] 
                    totalCalc += data["totalMoney"]
        return render_template("calculations.html", dateReport=dateReport, cost=cost, listDatas=listDatas, totalCalc=totalCalc)
    else:
        return apology("go back")