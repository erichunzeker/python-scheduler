from flask import Flask, render_template, request
import re
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def root_page():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run()