import pandas as pd

from config import todays_date, file_directory_input, file_directory_output, file_name_basic, file_name_sale, file_name_prices, file_name_price_LT, \
     file_name_art_dubl, cols_in_vesta
from price_processing import def_price_df_my, def_price_sale, def_price_my_to_xlsx, def_price_public_basic_to_xlsx, def_to_zakroma
from pricing_basic import def_pricing_basic
from pricing_sale import def_pricing_sale

#Преобразование прайсов СТ функциями и формирование "мой прайс" и "публичный прайс"
#функция преобразования прайса СТ в "мой прайс"
price_my_to_xlsx = def_price_df_my(file_directory_input, file_name_basic)
#функция преобразования прайса СТ в "публичный прайс" и выгрузка его в директорию
price_public_sale_to_xlsx = def_price_sale(file_directory_input, file_name_sale)
#"мой прайс" - выгрузка его в директорию
def_price_my_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_output)
#"публичный прайс" - выгрузка его в директорию
def_price_public_basic_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_output)

#Формирование файлов ценообразования
#Загружаем файл с ценами из карточки ценообразования в Весте
prices_in_vesta = pd.read_excel(file_directory_input+file_name_prices, usecols=cols_in_vesta)
#Загружаем файл дублей
art_dubl_df = pd.read_excel(file_directory_input+file_name_art_dubl)
#Загружаем базовый Прайс-лист_СТ_todays_date_мой, типа Прайс-лист_СТ_2022-09-12_мой
prices_LT = pd.read_excel(file_directory_output+file_name_price_LT, sheet_name=todays_date)
#Загружаем распродажный Прайс-лист_СТ_todays_date_мой, типа Прайс-лист_СТ_2022-09-12_мой
prices_LT_sale = pd.read_excel(file_directory_output+file_name_price_LT, sheet_name=todays_date+'(Р)')
#Обработка базового прайса функцией, выгрузка файла ценообразования базового прайса для загрузки в VESTA
def_pricing_basic(prices_in_vesta, art_dubl_df, prices_LT, file_directory_output)
#Обработка распродажного прайса функцией, выгрузка файла ценообразования прайса распродажи для загрузки в VESTA
def_pricing_sale(prices_in_vesta, art_dubl_df, prices_LT_sale, file_directory_output)

#Формируем прайс в закрома
def_to_zakroma(price_my_to_xlsx, price_public_sale_to_xlsx, file_directory_output)