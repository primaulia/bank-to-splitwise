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
SPLITWISE_API_SECRET = os.environ.get("SPLITWISE_API_SECRET")

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

if __name__ == "__main__":
    app.run(debug=True)
