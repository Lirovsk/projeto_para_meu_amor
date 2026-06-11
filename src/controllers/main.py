from flask import Blueprint, render_template


app = Blueprint("main", __name__)


@app.route("/")
def index():
    return render_template("index.html")
