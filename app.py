from flask import Flask, render_template, request

from servicetags import resolve_ip

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        result = resolve_ip(user_input)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(degug=True)
