#Формирование прайс-листов

#библиотеки
import pandas as pd

# Основной прайс-лист
def def_price_df_my(file_directory_input, file_name_basic):
    price_df = pd.read_excel(file_directory_input+file_name_basic) #Прайс Световых базовый с их сайта
    index_drop_str = price_df.index[price_df['Unnamed: 0'] == 'Номенклатура'].tolist()
    price_df = price_df.iloc[index_drop_str[0]:]
    price_df.reset_index(inplace=True) #Обновляем индексы
    price_df = price_df.drop('index', axis=1) #Удаляем старые индексы
    columns = price_df.loc[0,:].tolist() #Список имён столбцов для формирования нового df без лишних пустых столбцов
    columns[columns.index('Наименование для печати в УПД')] = 'Наименование' #Наименование для печати УПД или Наименование для печати в УПД
    columns[columns.index('Цена с НДС')] = 'Базовый (РФ)' #Базовый (РФ) или Цена с НДС
    columns[columns.index('% скидки РОЦ')+1] = 'МРЦ' #% скидки РОЦ или РОЦ1
    columns[columns.index('Закупка дистрибьютора c НДС')] = 'Вход ЭКС' #Закупка дистрибьютора или Закупка дистрибьютора c НДС
    columns[columns.index('% скидки клиента')] = 'Скидка ЭКС' #Скидка ЭКС или % скидки клиента
    price_df.columns = columns #Назначаем шапку таблицы индексами столбцов

    #Определяем нужные для загрузки столбцы
    price_df = price_df[['Наименование', 'Артикул', 'Ед. изм.', 'Базовый (РФ)', 'МРЦ', 'Скидка ЭКС', 'Вход ЭКС']] #Записываем новый df с нужными столбцами
    price_df.drop(labels = [0, 1], axis = 0, inplace = True) #Удаляем ненужные строки 
    price_df.dropna(axis=0, how='all', inplace=True)
    price_df.reset_index(inplace=True) #Обновляем индексы
    price_df = price_df.drop('index', axis=1) #Удаляем старые индексы

    roznitsa_list = [] #Список для розничных цен
    for i in range(len(price_df)):
        roznitsa_list.append(round(price_df.iloc[i,4]*1.2+0.5, 0)) #МРЦ*1.2 +0.5 для округления в большую сторону
    price_df['Розница ЭКС'] = roznitsa_list
    return price_df

# Распродажа прайс-лист
def def_price_sale(file_directory_input, file_name_sale):
    price_df_sale = pd.read_excel(file_directory_input+file_name_sale) #Прайс Световых распродажа с их сайта
    index_drop_str = price_df_sale.index[price_df_sale['Unnamed: 0'] == 'Номенклатура'].tolist()
    price_df_sale = price_df_sale.iloc[index_drop_str[0]:]
    # price_df_sale.drop(labels = [0,1,2,3,4,5,6],axis = 0, inplace = True) #Удаляем ненужные строки
    price_df_sale.reset_index(inplace=True) #Обновляем индексы
    price_df_sale = price_df_sale.drop('index', axis=1) #Удаляем старые индексы
    columns = price_df_sale.loc[0,:].tolist() #Список колонок для нового df
    columns[columns.index('Наименование для печати в УПД')] = 'Наименование' #Наименование для печати УПД или Наименование для печати в УПД
    columns[columns.index('Цена с НДС')] = 'Базовый(РФ)/Вход ЭКС' #Базовый (РФ) или Цена с НДС

    price_df_sale.columns = columns #Назначаем шапку таблицы с индексами колонок
    price_df_sale = price_df_sale[['Наименование', 'Артикул', 'Ед. изм.', 'Базовый(РФ)/Вход ЭКС']] #Отбираем нужные колонки, записываем новый df

    price_df_sale.drop(labels = [0, 1], axis = 0, inplace = True) #Удаляем ненужные строки 
    price_df_sale.dropna(axis=0, how='all', inplace=True)
    price_df_sale.reset_index(inplace=True) #Обновляем индексы
    price_df_sale = price_df_sale.drop('index', axis=1) #Удаляем старые индексы

    roznitsa_list_sale = []
    for i in range(len(price_df_sale)):
        roznitsa_list_sale.append(round(price_df_sale.iloc[i,3]* 1.5+0.5, 0)) #'Базовый(РФ)/Вход ЭКС'*1.5 +0.5 для округления в большую сторону
    price_df_sale['Розница ЭКС'] = roznitsa_list_sale
    return price_df_sale
