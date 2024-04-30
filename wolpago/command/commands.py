import datetime


def command_attendance_notice(user: str, params: str):
    # valid params example: "오늘 16시", "내일 16시", "모레 16시", "오늘 16시 30분", "5월 1일 16시", "5월 2일 16시 30분"
    try:
        params = params.split()
        year = datetime.date.today().year
        month, day, remain_params = parse_month_day(params)
        hour, minute = parse_hour_minute(remain_params)
        if not is_time_future(year, month, day, hour, minute):
            return "과거의 시간은 설정할 수 없습니다.", {}
    except Exception as e:
        print(e)
        return (
            "올바른 형식의 날짜와 시간을 입력해주세요. 예시: '오늘 16시', '내일 9시 30분'",
            {},
        )

    msg = f"{user}님 {month}월 {day}일 {hour}시 {minute}분 출석예고"
    notifications = set_notifications(user, year, month, day, hour, minute)

    return msg, notifications


def is_time_future(year, month, day, hour, minute):
    current_timestamp = datetime.datetime.now().timestamp()
    timestamp = datetime.datetime(year, month, day, hour, minute).timestamp()
    return timestamp > current_timestamp


def set_notifications(user, year, month, day, hour, minute):
    notifications = {}
    timestamps = []
    # 정각 알림
    timestamp = datetime.datetime(year, month, day, hour, minute).timestamp()
    notifications[timestamp] = f"{user}님이 출석예정입니다."
    timestamps.append(timestamp)
    # 5분 전에 알림
    current_timestamp = datetime.datetime.now().timestamp()
    if timestamp - 300 > current_timestamp:
        notifications[timestamp - 300] = f"{user}님 5분 후 출석예정입니다."
    return notifications


def parse_month_day(params: list[str]):
    keywords_offset = {"오늘": 0, "내일": 1, "모레": 2}
    for keyword, offset in keywords_offset.items():
        if params[0] == keyword:
            date = datetime.date.today() + datetime.timedelta(days=offset)
            month = date.month
            day = date.day
            remain_params = params[1:]
            return month, day, remain_params

    month = params[0].rstrip("월")
    day = params[1].rstrip("일")
    remain_params = params[2:]
    return int(month), int(day), remain_params


def parse_hour_minute(remain_params: list[str]):
    hour = remain_params[0].rstrip("시")
    minute = remain_params[1].rstrip("분") if len(remain_params) == 2 else 0
    return int(hour), int(minute)
