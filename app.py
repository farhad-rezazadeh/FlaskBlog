from config import app

# Routs
from account.routes import *


@app.route("/")
def home():
    return render_template("blog/home.html")


if __name__ == "__main__":
    app.run()
