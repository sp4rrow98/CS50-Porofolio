import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    transactions = db.execute("SELECT *, SUM(quantity) as quantity FROM transactions WHERE user_id = ? GROUP BY symbol;", session["user_id"])
    userMoney = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    total_transactions = db.execute("SELECT SUM(total) FROM transactions ")[0]
    proba = total_transactions["SUM(total)"]
    total = 0
    
    for transaction in transactions:
        quote = lookup(transaction['symbol'])
        transaction['price'] = quote['price']
        transaction['total'] = transaction['price'] * transaction['quantity']
        total = proba + userMoney[0]['cash']

    # total = total + userMoney
    return render_template("index.html", transactions=transactions, userMoney=userMoney, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")
        
        try:
            shares = int(shares)
            if shares < 1:
                return apology("Enter positive value", 400)
        except ValueError:
            return apology("Enter positive value", 400)
            
        if quote == None or shares == None:
            return apology("Insert valid symbol")

        if shares == "":
            return apology("Enter positive value")

        sharePrice = float(quote["price"])
        cost =  int(shares) * sharePrice
        userCash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        balance = userCash[0]["cash"]
        now = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")

        if cost > balance:
            return apology("Not enough money")

        else:
            db.execute("UPDATE users SET cash = (cash - ?) WHERE id =?", cost, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, stock, symbol, quantity, value, date, type, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",session["user_id"], str(quote["name"]), str(quote["symbol"]), shares, sharePrice, now, "buy", cost)
        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT type, date, symbol, value, quantity FROM transactions")
        
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Please enter a symbol", 400)
        else:
            symbol = quote.get("symbol")
            price = quote.get("price")
            return render_template("quoted.html", symbol=symbol, price = usd(price))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""


    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        name = request.form.get("username")
        usernames = db.execute("SELECT username FROM users WHERE username = ?", name)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if len(usernames) > 0:
            return apology("Insert another username", 400)
        if not request.form.get("username") or name in usernames:
            return apology("Insert a name", 400)
        if name == None or name in usernames or name == False:
            return apology("Must provide username", 400)
        if not password == confirmation:
            return apology("Must provide password", 400)
        if not request.form.get("password"):
            return apology("Insert a valid password")
        else:
            db.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)", name, generate_password_hash(password), 10000)
            return render_template("login.html")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        rows = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", session["user_id"])

        for row in rows:
            symbol = row["symbol"]
        return render_template("sell.html", rows=rows)

    if request.method == "POST":

        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("Insert shares and symbol to sell")

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        stocks = db.execute("SELECT SUM(quantity) as quantity, value FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]

        if int(shares) <= 0:
            return apology("You need positive shares")

        elif int(shares) > stocks["quantity"]:
            return apology("Not enough shares")

        else:
            price = lookup(symbol)["price"]
            totalPrice = price * int(shares)
            now = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")
            client_cash = db.execute("SELECT cash from users WHERE id =?", session["user_id"])[0]["cash"]
            db.execute("UPDATE users SET cash = ? WHERE id = ?", client_cash + totalPrice, session["user_id"])
            db.execute("INSERT INTO transactions (user_id, stock, symbol, quantity, value, date, type, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",session["user_id"], lookup(symbol)["name"], symbol, -int(shares), price, now, "sell", -totalPrice)
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
