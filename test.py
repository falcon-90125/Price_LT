import pandas as pd

file_name_basic = 'Прайс_CТ.xlsx' #Прайс Световых базовый с их сайта
file_directory_input = 'exchange/input/' #Директория для input'ов

price_df = pd.read_excel(file_directory_input+file_name_basic) #Прайс Световых базовый с их сайта
index_drop_str = price_df.index[price_df['Unnamed: 0'] == 'Номенклатура'].tolist()
price_df = price_df.iloc[index_drop_str[0]:]
price_df.reset_index(inplace=True) #Обновляем индексы
price_df = price_df.drop('index', axis=1) #Удаляем старые индексы
columns = price_df.loc[0,:].tolist() #Список имён столбцов для формирования нового df без лишних пустых столбцов
indices = [index for index, fruit in enumerate(columns) if fruit == 'Цена с НДС']
columns[columns.index('Наименование для печати в УПД')] = 'Наименование'
columns[indices[0]] = 'Базовый (РФ)'
columns[columns.index('% скидки клиента')] = 'Скидка ЭКС'
columns[indices[1]] = 'МРЦ'
columns[columns.index('Цена клиента с НДС')] = 'Вход ЭКС'

# #Переименовываем второй столбец 'Цена с НДС', который явл-ся МРЦ, в 'МРЦ'
# columns[columns.index('Цена с НДС', columns.index('Цена с НДС')+1)] = 'МРЦ'
price_df.columns = columns #Назначаем шапку таблицы индексами столбцов

#Определяем нужные для загрузки столбцы
price_df = price_df[['Наименование', 'Артикул', 'Ед. изм.', 'Базовый (РФ)', 'МРЦ', 'Скидка ЭКС', 'Вход ЭКС']] #Записываем новый df с нужными столбцами
price_df.drop(labels = [0, 1], axis = 0, inplace = True) #Удаляем ненужные строки 
price_df.dropna(axis=0, how='all', inplace=True)
price_df.reset_index(inplace=True) #Обновляем индексы
price_df = price_df.drop('index', axis=1) #Удаляем старые индексы

print(price_df.head(5))