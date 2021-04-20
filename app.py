from config import app


@app.route("/")
def home():
    return render_template("blog/home.html")


# Routs
from account.routes import *


if __name__ == "__main__":
    app.run()
