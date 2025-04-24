
# def get_date_interval(date_str: str, date_format = "%Y-%m-%d %H:%M:%S")-> list[str]:
#     """Функция возвращающая интервал времени"""
#     date_obj = datetime.strptime(date_str, date_format) # Получаем дату и форматируем
#     date_beginning = date_obj.replace(day = 1) # Меняем день
#
#     return[date_beginning.strftime("%d-%m-%Y %H.%M.%S"),
#            date_obj.strftime("%d-%m-%Y %H.%M.%S")] # Перевод даты обратно в строку