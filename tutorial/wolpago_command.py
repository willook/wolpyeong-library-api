from wolpago import Wolpago

wolpago = Wolpago()
msg = wolpago.execute("고맛사", "출석예고", "오늘 23시 51분")
print(msg)
msg = wolpago.execute("윤베리", "출석예고", "모레 16시 30분")
print(msg)
msg = wolpago.execute("월도", "출석예고", "5월 1일 4시 15분")
print(msg)

msg = wolpago.check_notification()
print(msg)
