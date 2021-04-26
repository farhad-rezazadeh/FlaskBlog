from flask import render_template
from config import app


@app.route("/test")
def admin():
    return render_template("account/adminlte/panel.html")
