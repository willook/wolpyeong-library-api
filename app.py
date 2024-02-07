from wpl_api import WPLAPI
from flask import Flask, render_template, request
from flask import send_file, make_response

app = Flask(__name__)

@app.route('/recent_holiday') # 접속하는 url
def index():
    wpl_api = WPLAPI()
    filename = wpl_api.save_recent_holiday_img()
    return send_file(filename, mimetype='image/jpg')

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="127.0.0.1", port="5000", debug=True)