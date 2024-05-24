import datetime

def ultimo_dia_util(data):
  data -= datetime.timedelta(days=1)
  while data.weekday() >= 5:
    data -= datetime.timedelta(days=1)
  return datetime.datetime.strftime(data,'%d/%m/%Y')