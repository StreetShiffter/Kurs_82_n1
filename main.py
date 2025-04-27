from config import PATH_FILE
from src.services import info_transaction_filter_phone
from src.views  import main_info
from src.reports  import get_dataframe



if __name__ == "__main__":
  date = "2018-04-22 18:16:00"
  date_decorator = "2018-04-15"
  category = "Супермаркеты"
  print(main_info(date))
  print(info_transaction_filter_phone(PATH_FILE))
  #Вызов функции spending_by_category с декоратором report_decorator из модуля reports
  print(get_dataframe(PATH_FILE))
