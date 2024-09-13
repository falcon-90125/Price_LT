import pandas as pd

from config import file_directory_input, file_name_basic

price_df = pd.read_excel(file_directory_input+file_name_basic) #Прайс Световых базовый с их сайта
index_drop_str = price_df.index[price_df['Unnamed: 0'] == 'Номенклатура'].tolist()
price_df = price_df.iloc[index_drop_str[0]:]
price_df.reset_index(inplace=True) #Обновляем индексы
price_df = price_df.drop('index', axis=1) #Удаляем старые индексы
columns = price_df.loc[0,:].tolist() #Список имён столбцов для формирования нового df без лишних пустых столбцов
# indices = [index for index, fruit in enumerate(columns) if fruit == 'Цена с НДС']
columns[columns.index('Наименование для печати УПД')] = 'Наименование'
columns[columns.index('РОЦ1')+1] = 'МРЦ'
columns[columns.index('Закупка дистрибьютора')] = 'Скидка ЭКС'
# columns[indices[1]] = 'МРЦ'
columns[columns.index('Закупка дистрибьютора')+1] = 'Вход ЭКС'