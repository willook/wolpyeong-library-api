import datetime
from queue import PriorityQueue

from wolpago.command.commands import command_attendance_notice


class Wolpago:
    def __init__(self):
        self.alarm_queue = PriorityQueue()
        pass

    def update_notification(self, alarms: dict):
        for timestamp, msg in alarms.items():
            self.alarm_queue.put((timestamp, msg))

    def check_notification(self) -> str:
        current_timestamp = datetime.datetime.now().timestamp()
        msg_list = []
        while not self.alarm_queue.empty():
            timestamp, msg = self.alarm_queue.get()
            if timestamp > current_timestamp:
                self.alarm_queue.put((timestamp, msg))
                break
            msg_list.append(msg)
        return "\n".join(msg_list)

    def execute(self, user: str, cmd: str, params: str) -> str:
        if cmd == "출석예고":
            # valid params example: "오늘 16시", "내일 16시", "모레 16시", "오늘 16시 30분", "5월 1일 16시"
            msg, alarms = command_attendance_notice(user, params)
            self.update_notification(alarms)
            return msg
        elif cmd == "휴관일":
            return
        elif cmd == "tmi":
            return
        else:
            return f"아직 {cmd}은/는 구현되지 않은 기능입니다."
