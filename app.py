"""
Runs the flask app for the servicetags checker application
"""

from flask import Flask, render_template, request

from servicetags import resolve_ip

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Simply takes user input and passes to the servicetags
    module, resolve_ip function
    """
    result = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        result = resolve_ip(user_input)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(degug=True)
