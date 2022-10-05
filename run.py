import pandas as pd
from price_processing import def_price_df_my, def_price_sale, def_price_my_to_xlsx, def_price_public_basic_to_xlsx
from pricing_basic import def_pricing_basic
from pricing_sale import def_pricing_sale
from to_zakroma import def_to_zakroma
# import openpyxl
# from openpyxl.styles.numbers import BUILTIN_FORMATS

#используем движок xlsxwriter для создания объекта writer. Он и передается функции to_excel().
#pip install openpyxl xlsxwriter xlrd

todays_date = '2022-09-30'

#Директории для прайс-листов
file_directory_resalts = 'E:\Соколов Алексей\Documents\ПОСТАВЩИКИ I\СВЕТОВЫЕ ТЕХНОЛОГИИ\Прайс-листы Световые технологии/'
file_name = todays_date+'_Прайс_CТ.xlsx'
file_name_sale = todays_date+'_Прайс_CТ_распродажа.xlsx'

#Директории для файлов ценообразования
file_directory_prices_in_vesta = 'E:\Соколов Алексей\Documents\Номенклатура\Цены\Световые Технологии/'
file_name_prices = 'Цены_СТ_'+todays_date+'.xlsx' #Выгрузить из карточки ценообразования по Поставщику МГК Световые Технологии ООО, код 81948
file_name_price_LT = 'Прайс-лист_СТ_'+todays_date+'_мой.xlsx'
file_name_art_dubl = 'Артикул_дубль.xlsx'

#Директории закромов
file_directory_to_zakroma = 'W:\Документы_Общие\Остатки поставщиков\ВД\81948 Световые технологии\Цены/'


#Загружаем основной прайс и распродажу
price_df = pd.read_excel(file_directory_resalts+file_name)
price_df_sale = pd.read_excel(file_directory_resalts+file_name_sale)

#Обработка прайсов функциями
price_my_to_xlsx = def_price_df_my(price_df)
price_public_sale_to_xlsx = def_price_sale(price_df_sale)

def_price_my_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts)
def_price_public_basic_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts)


# #Загружаем файл с ценами из карточки ценообразования
# prices_in_vesta = pd.read_excel(file_directory_prices_in_vesta+file_name_prices)
# prices_in_vesta.drop(prices_in_vesta.columns[[0, 1, 3, 5, 6, 7, 8,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,32]], axis='columns', inplace=True)
# #Загружаем файл дублей
# art_dubl_df = pd.read_excel(file_directory_prices_in_vesta+file_name_art_dubl)
# #Загружаем Прайс-лист_СТ_todays_date_мой, типа Прайс-лист_СТ_2022-09-12_мой
# prices_LT = pd.read_excel(file_directory_resalts+file_name_price_LT, sheet_name=todays_date)
# #Обработка прайса функцией, выгрузка файла ценообразования для закачки в VESTA
# nomenclature_change_basic = def_pricing_basic(prices_in_vesta, art_dubl_df, prices_LT)
# nomenclature_change_basic.to_excel(file_directory_prices_in_vesta + 'Закачка Световые Технологии' + file_name_prices[7:-5] +'_basic.xlsx', sheet_name='ActualCeni', index=False)

# #Загружаем Прайс-лист_СТ_todays_date_мой, типа Прайс-лист_СТ_2022-09-12_мой
# prices_LT_sale = pd.read_excel(file_directory_resalts+file_name_price_LT, sheet_name=todays_date+'(Р)')
# #Обработка прайса функцией, выгрузка файла ценообразования для закачки в VESTA
# nomenclature_change_sale = def_pricing_sale(prices_in_vesta, art_dubl_df, prices_LT_sale)
# nomenclature_change_sale.to_excel(file_directory_prices_in_vesta + 'Закачка Световые Технологии' + file_name_prices[7:-5] +'_sale.xlsx', sheet_name='ActualCeni', index=False)


price_to_zakroma = def_to_zakroma(price_my_to_xlsx, price_public_sale_to_xlsx)
price_to_zakroma.to_excel(file_directory_resalts + 'Прайс Световые технологии с распродажей - в закрома' + file_name_prices[7:-5] +'.xlsx', index=False)
# price_to_zakroma.to_excel(file_directory_to_zakroma + 'Прайс Световые технологии с распродажей - в закрома' + file_name_prices[7:-5] +'.xlsx', index=False)