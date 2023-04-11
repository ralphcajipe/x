import os

from cs50 import SQL
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.apps import custom_app_context as pwd_context

from helpers import apology, login_required, lookup, usd

# Creating a Flask application object.
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """
    Make sure API requests aren't cached.
    :param response:
    :return:
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# This is a filter that allows us to use the usd function in the jinja
# templates.
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# This is a check to make sure that the API_KEY is set.
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# Homepage
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # The above code is selecting the symbol and sum of shares from the
    # transactions table where the user_id is equal to the user_id in the
    # session. It is grouping the results by symbol and having the sum of shares
    # greater than 0.
    rows = db.execute(
        "SELECT symbol, SUM(shares) FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING SUM(shares) > 0",
        user_id=session["user_id"],
    )

    # Creating an empty list called holdings and a variable called all_total and
    # setting it to 0.
    holdings = []
    all_total = 0

    # The above code is looping through the rows of the database and appending
    # the holdings list with the symbol, name, shares, price, and total.
    for row in rows:
        stock = lookup(row["symbol"])
        sum_value = stock["price"] * row["SUM(shares)"]
        holdings.append(
            {
                "symbol": stock["symbol"],
                "name": stock["name"],
                "shares": row["SUM(shares)"],
                "price": usd(stock["price"]),
                "total": usd(sum_value),
            }
        )
        all_total += stock["price"] * row["SUM(shares)"]

    # Selecting the cash from the users table where the id is equal to the
    # user_id.
    rows = db.execute(
        "SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"]
    )
    cash = rows[0]["cash"]
    all_total += cash

    # The above code is rendering the index.html template, and passing in the
    # variables holdings, cash, and all_total.
    return render_template(
        "index.html", holdings=holdings, cash=usd(cash), all_total=usd(all_total)
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # Ensure shares is a valid integer
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a whole number")

        # Ensure shares is greater than 0
        if shares <= 0:
            return apology("shares must be greater than 0")

        # Ensure stock exists
        if not request.form.get("symbol"):
            return apology("must provide an existing symbol")

        # Lookup function
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)
        if stock is None:
            return apology("symbol does not exist")

        # Value of transaction
        transactionb = shares * stock["price"]

        # Ensure user has enough cash
        rows = db.execute(
            "SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"]
        )
        cash = rows[0]["cash"]
        if transactionb > cash:
            return apology("not enough cash")

        # Update cash
        db.execute(
            "UPDATE users SET cash=cash-:transactionb WHERE id=:user_id",
            transactionb=transactionb,
            user_id=session["user_id"],
        )

        # Update transactions
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) \
                    VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=stock["symbol"],
            shares=shares,
            price=stock["price"],
        )

        flash("Bought!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT symbol, shares, price, transacted FROM transactions WHERE user_id=:user_id",
        user_id=session["user_id"],
    )
    for i in range(len(transactions)):
        transactions[i]["price"] = usd(transactions[i]["price"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"),
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure name of stock was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        # Use the lookup function
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        # Check if stock is valid
        if stock == None:
            return apology("Stock symbol not valid", 400)

        # If its valid
        else:
            return render_template(
                "quoted.html",
                stockSpec={"name": stock["symbol"], "price": usd(stock["price"])},
            )

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure username is unique
        elif (
            len(
                db.execute(
                    "SELECT username FROM users WHERE username = ?",
                    request.form.get("username"),
                )
            )
            != 0
        ):
            return apology("username taken", 400)

        elif len(request.form.get("password")) < 8:
            return apology("password must have at least 8 characters", 400)

        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match confirmation", 400)

        # Add username to database
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure stock was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares")

        # Ensure shares is greater than 0
        elif int(request.form.get("shares")) < 0:
            return apology("must provide a valid number of shares")

        # Ensure stock exists
        if not request.form.get("symbol"):
            return apology("must provide an existing symbol")

        # Lookup function
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        rows = db.execute(
            "SELECT symbol, SUM(shares) FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING SUM(shares) > 0",
            user_id=session["user_id"],
        )

        # Value of transaction
        shares = int(request.form.get("shares"))
        for row in rows:
            if row["symbol"] == symbol:
                if shares > row["SUM(shares)"]:
                    return apology("you're doing something wrong")

        transaction = shares * stock["price"]

        # Check if user has enough cash for transaction
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id=:id", id=session["user_id"]
        )
        cash = user_cash[0]["cash"]

        # Subtract user_cash by value of transaction
        updt_cash = cash + transaction

        # Update how much left in his account (cash) after the transaction
        db.execute(
            "UPDATE users SET cash=:updt_cash WHERE id=:id",
            updt_cash=updt_cash,
            id=session["user_id"],
        )
        # Update de transactions table
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=stock["symbol"],
            shares=-1 * shares,
            price=stock["price"],
        )
        flash("Sold!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        rows = db.execute(
            "SELECT symbol FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING SUM(shares) > 0",
            user_id=session["user_id"],
        )
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])


def errorhandler(e):
    """
    If the error is not an HTTPException, then it is an InternalServerError

    :param e: The exception that was raised
    :return: The errorhandler function is being returned.
    """
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# The above code is a for loop that is iterating through the
# default_exceptions list. The app.errorhandler(code) is a decorator that is
# used to register the errorhandler function as a handler for the given
# exception code.
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
