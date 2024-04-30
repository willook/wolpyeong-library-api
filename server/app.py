import flask
from flask import Flask, render_template, request
from flask import send_file, make_response

from wolpago.entity.wolpago import Wolpago

app = Flask(__name__)
wolpago = Wolpago()


@app.route("/heartbeat", methods=["GET"])
def handle_get_request():
    return "Hello, GET request"


@app.route("/command", methods=["POST"])
def handle_post_request():
    data = flask.request.get_json()

    user: str = data["user"]
    message: str = data["message"]
    print(f"Received message: {message}")

    # Process the data received in the POST request
    if message[0] != "!":
        return "명령어는 '!'로 시작해야합니다. 예) '!출석예고 오늘 16시'"
    cmd, params = message[1:].split(" ", 1)
    response = wolpago.execute(user, cmd, params)
    return response


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="11100", debug=True)
