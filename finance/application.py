import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = float(rows[0]["cash"])
    stocks = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = :user_id
        GROUP BY symbol
        HAVING shares > 0
        """,
        user_id=session["user_id"])
    portfolio = []
    total_stock_value = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote is None:
            continue
        price = float(quote["price"])
        shares = int(stock["shares"])
        total = price * shares

        total_stock_value += total

        portfolio.append({
            "symbol": stock["symbol"],
            "shares": shares,
            "price": price,
            "total": total
        })
    grand_total = cash + total_stock_value
    
    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbols = request.form.get("symbol")
        numb = request.form.get("shares")
        stock = lookup(symbols)
        if stock is None:
            return apology("API have some problems", 400)
        if not numb.isdigit() or numb == 0:
            return apology("Count must be a positive integer", 400)
        else:
            rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
            cash = rows[0]["cash"]
            price = float(stock["price"])
            total_price = price * int(numb)
            if total_price > float(cash):
                return apology("You haven't money for this operation", 400)
            else:
                db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=cash - total_price, id=session["user_id"])
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=stock["symbol"],
            shares=numb,
            price=price)
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/check", methods=["POST"])
def check():
    """Return true if username available, else false"""
    username = request.form.get("username")
    if not username:
        return False
    if len(username) <= 0:
        return False
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    if len(rows) == 0:
        return True



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        """
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = :user_id
        ORDER BY transacted DESC
        """,
        user_id=session["user_id"])
    for transaction in transactions:
        if transaction["shares"] > 0:
            transaction["type"] = "BUY"
        else:
            transaction["type"] = "SELL"
            transaction["shares"] = abs(transaction["shares"])
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
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/changpass", methods=["GET", "POST"])
@login_required
def changpass():
    """Change password for user"""
    if request.method == "POST":
        oldpassword = request.form.get("oldpassword")
        newpassword = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")
        # Ensure password was submitted
        if not newpassword or not oldpassword :
            return apology("must provide password", 403)
        if not confirmation:
            return apology("must provide confirmation", 403)
        if confirmation != newpassword:
            return apology("passwords must match", 403)

        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Check old password
        if not check_password_hash(rows[0]["hash"], oldpassword):
            return apology("old password is incorrect", 403)

        # Add new password in database
        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id",
        user_id=session["user_id"],
        hash=generate_password_hash(newpassword))

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("changpass.html")

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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if not symbol or stock is None:
            return apology("Must be provide correct symbol", 400)
        else:
            return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not check():
            return apology("must provide username", 403)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)
        if not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match", 403)

        # Add username and password in database
        password = request.form.get("password")
        user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                          username=request.form.get("username"), hash=generate_password_hash(password))

        # Remember which user has logged in
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must select symbol", 400)
        rows = db.execute(
            """
            SELECT SUM(shares) AS shares
            FROM transactions
            WHERE user_id = :user_id AND symbol = :symbol
            GROUP BY symbol
            """,
            user_id=session["user_id"],
            symbol=symbol)
        if len(rows) == 0 or rows[0]["shares"] <= 0:
            return apology("you do not own this stock", 400)
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be positive", 400)
        except (ValueError, TypeError):
            return apology("shares must be positive", 400)

        owned_shares = rows[0]["shares"]
        if shares > owned_shares:
            return apology("you don't have so much", 400)
        stock = lookup(symbol)
        price = float(stock["price"])
        cash_row = db.execute( "SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = float(cash_row[0]["cash"])
        db.execute( "UPDATE users SET cash = :cash WHERE id = :id", cash=cash + shares * price, id=session["user_id"])
        db.execute(
            """
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (:user_id, :symbol, :shares, :price)
            """,
            user_id=session["user_id"],
            symbol=symbol,
            shares=-shares,
            price=price
        )

        return redirect("/")
    else:
        symbols = db.execute(
        """
        SELECT symbol
        FROM transactions
        WHERE user_id = :user_id
        GROUP BY symbol
        HAVING SUM(shares) > 0
        """,
        user_id=session["user_id"])
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
