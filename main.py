from config import PATH_FILE, FILE_JSON
from src.services import info_transaction_filter_phone
from src.views  import main_info


if __name__ == "__main__":
  #print(main_info("2018-04-22 18:16:00"))
  print(info_transaction_filter_phone(PATH_FILE))
