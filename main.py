from config import PATH_FILE, FILE_JSON, PATH_FILE_UNIQUE
from src.services import info_transaction_filter_phone
from src.utils import get_phone_number
from src.views  import main_info


if __name__ == "__main__":
  print(main_info("2018-04-22 18:16:00"))
  # print(info_transaction_filter_phone(PATH_FILE))
  # print(get_phone_number(PATH_FILE))
