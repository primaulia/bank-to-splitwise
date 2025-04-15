import os
from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
from splitwise import Splitwise
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

# Load Splitwise credentials from environment variables
SPLITWISE_CONSUMER_KEY = os.environ.get("SPLITWISE_CONSUMER_KEY")
SPLITWISE_CONSUMER_SECRET = os.environ.get("SPLITWISE_CONSUMER_SECRET")
SPLITWISE_API_KEY = os.environ.get("SPLITWISE_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "statement" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["statement"]
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file:
            df = pd.read_csv(file)
            # Here: categorize and sync to Splitwise (to be implemented)
            flash(f"Parsed {len(df)} transactions. (Splitwise sync not yet implemented)")
            return render_template("index.html", transactions=df.to_dict(orient="records"))
    return render_template("index.html")

@app.route("/splitwise/callback", methods=["POST"])
def splitwise_callback():
    # You can log or process the incoming webhook data here
    data = request.json or request.form
    print("Received Splitwise webhook:", data)
    # Respond with 200 OK so Splitwise knows you received it
    return "Webhook received", 200

@app.route("/test-splitwise-expense")
def test_splitwise_expense():
    # Initialize Splitwise client (OAuth1, using consumer key/secret and API key)
    s = Splitwise(
        SPLITWISE_CONSUMER_KEY,
        SPLITWISE_CONSUMER_SECRET,
        api_key=SPLITWISE_API_KEY
    )
    # Get your user ID
    current_user = s.getCurrentUser()
    user_id = current_user.getId()
    # Create a simple expense: you paid $1.00 for yourself
    from splitwise.expense import Expense, ExpenseUser
    expense = Expense()
    expense.setCost("1.00")
    expense.setDescription("Test Expense from Flask")
    user = ExpenseUser()
    user.setId(user_id)
    user.setPaidShare("1.00")
    user.setOwedShare("1.00")
    expense.addUser(user)
    created_expense, errors = s.createExpense(expense)
    if errors:
        return f"Error: {errors}", 400
    return f"Expense created! ID: {created_expense.getId()}"

if __name__ == "__main__":
    app.run(debug=True)
