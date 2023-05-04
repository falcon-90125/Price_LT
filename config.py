with open('exchange\input\data_price.txt', 'r') as f:  # считываем дату прайса из файла
  todays_date = f.read()
  f.close()

file_directory_input = 'exchange/input/' #Директория для input'ов
file_name_basic = 'Прайс_CТ.xlsx' #Прайс Световых базовый с их сайта
file_name_sale = 'Прайс_CТ_распродажа.xlsx' #Прайс Световых распродажный с их сайта
file_name_prices = 'Цены_СТ_из_Весты.xlsx' #Выгрузить из карточки ценообразования по Поставщику МГК Световые Технологии ООО, код 81948
file_name_art_dubl = 'Артикул_дубль.xlsx' #Файл дублей артикулов, которых уже нет в прайсе, но есть в Весте

file_directory_output = 'exchange/output/' #Директория для output'ов
file_name_price_LT = 'Прайс-лист_СТ_'+todays_date+'_мой.xlsx'

#Загружаем файл с ценами из карточки ценообразования
cols_in_vesta = ['Код', 'Артикул', 'ТарифПост валюта.', 'Розница', 'МРЦ', 'Актуальная для транзитов']