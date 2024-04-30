import json
import requests


def send_post_request():
    url = "http://jonghwa.actnova.io:11100/command"
    user = "고맛사"
    msg = "!출석예고 오늘 09시 30분"
    payload = {"message": msg, "user": user}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"[{response.status_code}] {response.text}")


send_post_request()
