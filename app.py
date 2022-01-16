import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///netflix.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# ----------------------------------------------- DataBase ----------------------------------------------- #
'''
CREATE TABLE movies (id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    type TEXT NOT NULL,
                    image_file TEXT NOT NULL,
                    video_file TEXT NOT NULL,
                    eps_num INTEGER NOT NULL,
                    season_num INTEGER NOT NULL,
                    rate FLOAT NOT NULL,
                    cat1 TEXT NOT NULL,
                    cat2 TEXT NOT NULL,
                    cat3 TEXT NOT NULL,
                    PRIMARY KEY(id)
                    );

CREATE TABLE users (
                id INTEGER,
                username TEXT NOT NULL,
                email TEXT ,
                hash TEXT NOT NULL,
                UNIQUE (username),
                UNIQUE (email),
                PRIMARY KEY(id)
            );

CREATE TABLE mylist (
                movies_id INTEGER,
				user_id INTEGER,
                FOREIGN KEY(movies_id) REFERENCES movies(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

'''
# ----------------------------------------------- globalQuery ----------------------------------------------- #
globalQuery = db.execute("SELECT * FROM movies")

# ----------------------------------------------- home ----------------------------------------------- #
@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        currntUser = session["user_id"]
        print('currntUser: ',currntUser)
        input = request.form.get("mylist")
        print('input: ',input)
        query = db.execute("Select * FROM mylist Where movies_id = ?", input)
        print('query: ',query)
        if not query:
            db.execute("INSERT INTO mylist (movies_id, user_id) VALUES(?, ?)", input, currntUser)
        else:
            pass
        return redirect('/mylist')

    if request.method == "GET":
        # print(session["user_id"])
        # currntUser = session["user_id"]
        data = globalQuery[0:10]
        movies = []
        shows = []
        action=[]
        drama=[]
        comedy=[]
        fantasy=[]
        scifi=[]
        for i in globalQuery:
            if i['type'] == 'Movie':
                if len(movies) < 10 :
                    movies.append(i)

            if i['type'] == 'Series':
                if len(shows) < 10:
                    shows.append(i)

            if i['cat1'] == 'Action' or i['cat2'] == 'Action' or i['cat3'] == 'Action':
                if len(action) < 10:
                    action.append(i)

            if i['cat1'] == 'Drama' or i['cat2'] == 'Drama' or i['cat3'] == 'Drama':
                if len(drama) < 10:
                    drama.append(i)

            if i['cat1'] == 'Comedy' or i['cat2'] == 'Comedy' or i['cat3'] == 'Comedy':
                if len(comedy) < 10:
                    comedy.append(i)

            if i['cat1'] == 'Fantasy' or i['cat2'] == 'Fantasy' or i['cat3'] == 'Fantasy':
                if len(fantasy) < 10:
                    fantasy.append(i)

            if i['cat1'] == 'Sci-Fi' or i['cat2'] == 'Sci-Fi' or i['cat3'] == 'Sci-Fi':
                if len(scifi) < 10:
                    scifi.append(i)
            
        print(len(movies))
        context = {
            'data':data,
            'movies':movies,
            'shows':shows,
            'action':action,
            'drama':drama,
            'comedy':comedy,
            'fantasy':fantasy,
            'scifi':scifi
        }
        return render_template("home.html", data=context )
# ----------------------------------------------- movies ----------------------------------------------- #
@app.route("/movies", methods=["GET", "POST"])
@login_required
def movies():
    if request.method == "POST":
        pass

    if request.method == "GET":
        # currntUser = session["user_id"]
        movies = []
        for i in globalQuery:
            if i['type'] == 'Movie':
                if len(movies) < 10 :
                    movies.append(i)

        context = {
            'movies':movies,
        }

        return render_template("movies.html", data=context )
# ----------------------------------------------- tvshows ----------------------------------------------- #
@app.route("/tvshows", methods=["GET", "POST"])
@login_required
def tvshows():
    if request.method == "POST":
        pass

    if request.method == "GET":
        currntUser = session["user_id"]
        shows = []

        for i in globalQuery:
            if i['type'] == 'Series':
                if len(shows) < 10 :
                    shows.append(i)

        context = {
            'shows':shows,
        }
        return render_template("tvshows.html", data=context )
# ----------------------------------------------- mylist ----------------------------------------------- #
@app.route("/mylist", methods=["GET", "POST"])
@login_required
def mylist():
    if request.method == "POST":
        currntUser = session["user_id"]
        input = request.form.get("mylist")
        query = db.execute("Delete from mylist where movies_id = ? and user_id = ?",input,currntUser)
        return redirect('/mylist')

    if request.method == "GET":
        currntUser = session["user_id"]
        print(currntUser)
        list=[]
        query = db.execute("Select * from mylist where user_id = ? ",currntUser)
        for i in query :
            list.append(i['movies_id'])
        print(list)
        data = db.execute("Select * from movies where id in (?) ",list)
        print(data)

        # for i in globalQuery:

        context = {
            'data':data,
        }

        return render_template("mylist.html", data=context )
# ----------------------------------------------- terms ----------------------------------------------- #
@app.route("/terms", methods=["GET", "POST"])
@login_required
def terms():
    if request.method == "POST":
        pass

    if request.method == "GET":
        return render_template("terms.html")
# ----------------------------------------------- about ----------------------------------------------- #
@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    if request.method == "POST":
        pass

    if request.method == "GET":
        return render_template("about.html")
# ----------------------------------------------- preview ----------------------------------------------- #
# /preview
@app.route("/preview", methods=["GET", "POST"])
@login_required
def preview():
    if request.method == "POST":
        input = request.form.get("play")
        # print(type(input))
        # rows = db.execute("SELECT * FROM movies WHERE id = ?", input)
        rows = []
        for i in globalQuery:
            # print('input',input)
            # print(type(i['id']))
            if i['id'] == int(input) :
                rows.append(i)
        # print(rows)
        row = rows[0]
        return render_template("preview.html" , data=row)
            
    if request.method == "GET":
        pass

# ----------------------------------------------- login ----------------------------------------------- #

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # print('rows: ', rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        # if len(rows) != 1 :
            return apology("log in error", 403)

        # Remember which user has logged in
        try:
            session["user_id"] = rows[0]["id"]
        except:
            print('no session was created motherfucker')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# ----------------------------------------------- register ----------------------------------------------- #


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        """Register user"""
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm =request.form.get("confirmation")

        if password != password_confirm :
            return apology("must provide username", 400)

        password = generate_password_hash(request.form.get("password"))
        # print(password)
        session.clear()


        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) >= 1 :
            print('error line 151 checkpass')
            return apology("invalid username and/or password", 400)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Remember which user has logged in
        try:
            session["user_id"] = rows[0]["id"]
        except:
            print('no session was created motherfucker')

        return redirect ('/')

    if request.method == "GET":
        return render_template("register.html")

# ----------------------------------------------- logout ----------------------------------------------- #

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# ---------------------------------------------------------------------------------------------- #