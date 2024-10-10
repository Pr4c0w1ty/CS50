import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    id = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    grouped_transactions = {}
    acc_value = id[0]["cash"]
    print("HALO TO TU ", acc_value)
    for transaction in transactions:
        symbol = transaction['symbol']
        shares = transaction['shares']
        price_info = lookup(symbol)
        if price_info and 'price' in price_info:
            price = price_info['price']
            value = shares * price
            if symbol in grouped_transactions:
                grouped_transactions[symbol]['shares'] += shares
                grouped_transactions[symbol]['value'] += value
                acc_value += grouped_transactions[symbol]['value']
            else:
                grouped_transactions[symbol] = {
                    'symbol': symbol,
                    'shares': shares,
                    'price': round(price, 2),
                    'value': round(value, 2)
                }
                acc_value += grouped_transactions[symbol]['value']
    acc_value = round(acc_value, 2)
    formatted_cash = "{:,.2f}".format(id[0]['cash'])
    return render_template("index.html", id=id, grouped_transactions=grouped_transactions, acc_value=acc_value, formatted_cash=formatted_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("You must enter a stock symbol", 400)
        number = request.form.get("shares")
        try:
            number = int(number)
            if number <= 0:
                return apology("Number of shares must be a positive integer", 400)
        except ValueError:
            return apology("You must enter a valid number of shares to buy", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Symbol doesn't exist or API error", 400)
        cost = number * stock['price']
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_amount = cash[0]['cash']
        stock_cost = stock['price']
        new_balance = cash_amount - stock_cost
        if new_balance < 0:
            return apology("too poor :(", 400)
        cash_amount = cash_amount - cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   round(cash_amount, 2), session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], stock['symbol'], number, stock['price'])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
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
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("You must enter a stock symbol", 400)

        stock_info = lookup(symbol)
        if stock_info and 'price' in stock_info:
            stock_info = lookup(symbol)['price']
            return render_template("quote.html", stock=stock_info)
        else:
            return apology("Symbol doesn't exist or API error", 400)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must provide confirmation", 400)

        elif not password == confirmation:
            return apology("passwords doesn't match", 400)
        # Check if username already exists
        result = db.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if list(result):  # Convert to list to see if any rows exist
            return apology("username already exists", 400)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        try:
            number = int(request.form.get("shares"))
            if number <= 0:
                flash("Number of shares must be a positive integer.", "error")
                return apology("Number of shares must be a positive integer", 400)
        except ValueError:
            flash("You must enter a valid number of shares to sell.", "error")
            return apology("You must enter a valid number of shares to sell", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Stock symbol does not exist.", 400)

        # Aggregate shares owned
        shares_owned = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        shares_owned = shares_owned[0]['total_shares'] if shares_owned[0]['total_shares'] else 0

        if number > shares_owned:
            return apology("You do not own enough shares to complete this transaction.", 400)

        sale_value = number * stock['price']
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
        new_cash_balance = cash + sale_value

        # Update cash balance and record transaction
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   round(new_cash_balance, 2), session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, -number, stock['price'])

        flash("Shares sold successfully!", "info")
        return redirect("/")
    else:
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", stocks=stocks)
