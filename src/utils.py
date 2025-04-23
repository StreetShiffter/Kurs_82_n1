from datetime import datetime



def greet_func()-> str:
    """Функция определяющая время суток и приветствует"""
    time_now = datetime.now().hour
    if 6 < time_now <= 12:
        greet = "Доброе утро"
    elif 12 < time_now <= 18:
            greet = "Добрый день"
    elif 18 < time_now <= 23:
            greet = "Добрый вечер"
    else:
        greet = "Доброй ночи"

    return greet

def get_date_interval(date_str: str, date_format: str =  "%Y-%m-%d %H.%M.%S")-> list[str]:
    """Функция возвращающая интервал времени"""
    date_obj = datetime.strptime(date_str, date_format) # Получаем дату и форматируем
    date_beginning = date_obj.replace(day = 1) # Меняем день

    return[date_beginning.strftime("%d-%m-%Y %H.%M.%S"),
           date_obj.strftime("%d-%m-%Y %H.%M.%S"),] # Перевод даты обратно в строку