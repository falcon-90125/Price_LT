import pandas as pd
from price_processing import def_price_df_my, def_price_sale, def_price_my_to_xlsx, def_price_public_basic_to_xlsx
from pricing_basic import def_pricing_basic
from pricing_sale import def_pricing_sale
from to_zakroma import def_to_zakroma
from config import todays_date, file_directory_resalts, file_name, file_name_sale, file_directory_prices_in_vesta, file_name_prices, file_name_price_LT, file_name_art_dubl, file_directory_to_zakroma, cols_price_df, cols_price_df_sale, cols_in_vesta
#используем движок xlsxwriter для создания объекта writer. Он и передается функции to_excel().
#pip install openpyxl xlsxwriter xlrd


#Загружаем основной прайс
price_df = pd.read_excel(file_directory_resalts+file_name, usecols=cols_price_df)
#Загружаем прайс распродажи
price_df_sale = pd.read_excel(file_directory_resalts+file_name_sale, usecols=cols_price_df_sale)

# #Обработка прайсов функциями
price_my_to_xlsx = def_price_df_my(price_df) #функция из файла price_processing - преобразование в "мой прайс" и выгрузка его в директорию
price_public_sale_to_xlsx = def_price_sale(price_df_sale) #функция из файла price_processing - преобразование в "публичный прайс" и выгрузка его в директорию

def_price_my_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts)
def_price_public_basic_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts)


#Загружаем файл с ценами из карточки ценообразования
prices_in_vesta = pd.read_excel(file_directory_prices_in_vesta+file_name_prices, usecols=cols_in_vesta)

#Загружаем файл дублей
art_dubl_df = pd.read_excel(file_directory_prices_in_vesta+file_name_art_dubl)
#Загружаем Прайс-лист_СТ_todays_date_мой, типа Прайс-лист_СТ_2022-09-12_мой
prices_LT = pd.read_excel(file_directory_resalts+file_name_price_LT, sheet_name=todays_date)
#Обработка прайса функцией, выгрузка файла ценообразования для закачки в VESTA
nomenclature_change_basic = def_pricing_basic(prices_in_vesta, art_dubl_df, prices_LT)
nomenclature_change_basic.to_excel(file_directory_prices_in_vesta + 'Закачка Световые Технологии' + file_name_prices[7:-5] +'_basic.xlsx', sheet_name='ActualCeni', index=False)

#Загружаем Прайс-лист_СТ_todays_date_мой, типа Прайс-лист_СТ_2022-09-12_мой
prices_LT_sale = pd.read_excel(file_directory_resalts+file_name_price_LT, sheet_name=todays_date+'(Р)')
#Обработка прайса функцией, выгрузка файла ценообразования для закачки в VESTA
nomenclature_change_sale = def_pricing_sale(prices_in_vesta, art_dubl_df, prices_LT_sale)
nomenclature_change_sale.to_excel(file_directory_prices_in_vesta + 'Закачка Световые Технологии' + file_name_prices[7:-5] +'_sale.xlsx', sheet_name='ActualCeni', index=False)

#Формируем прайс в закрома
price_to_zakroma = def_to_zakroma(price_my_to_xlsx, price_public_sale_to_xlsx) # функция из to_zakroma
price_to_zakroma.to_excel(file_directory_resalts + 'Прайс Световые технологии с распродажей - в закрома' + file_name_prices[7:-5] +'.xlsx', index=False)
# price_to_zakroma.to_excel(file_directory_to_zakroma + 'Прайс Световые технологии с распродажей - в закрома' + file_name_prices[7:-5] +'.xlsx', index=False)