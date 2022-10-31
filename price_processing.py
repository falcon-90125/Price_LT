#Формирование прайс-листов

#библиотеки
import pandas as pd
import openpyxl
from openpyxl.styles.numbers import BUILTIN_FORMATS

#Основной прайс-лист
def def_price_df_my(price_df):
    price_df.drop(labels = [0,1,2,3,4,5,6,7,8],axis = 0, inplace = True) #Удаляем ненужные строки
    price_df.reset_index(inplace=True) #Обновляем индексы
    price_df = price_df.drop('index', axis=1) #Удаляем старые индексы
    cols = ['Номенклатура', 'Артикул', 'Ед. изм.', 'Базовый(РФ)', 'МРЦ', '% скидки ЭКС', 'Вход ЭКС'] #Вводим наименования столбцов
    price_df.columns = cols
    roznitsa_list = [] #Список для розничных цен
    for i in range(len(price_df)):
        roznitsa_list.append(round(price_df.iloc[i,4]*1.2+0.5, 0)) #МРЦ*1.2 +0.5 для округления в большую сторону
    price_df['Розница ЭКС'] = roznitsa_list
    price_df['Розница ЭКС'].number_format = openpyxl.styles.numbers.BUILTIN_FORMATS[2]
    return price_df

#Распродажа
def def_price_sale(price_df_sale):
    price_df_sale.drop(labels = [0,1,2,3,4,5,6,7,8],axis = 0, inplace = True) #Удаляем ненужные строки
    price_df_sale.reset_index(inplace=True) #Обновляем индексы
    price_df_sale = price_df_sale.drop('index', axis=1) #Удаляем старые индексы
    cols = ['Номенклатура', 'Артикул', 'Ед. изм.', 'Базовый(РФ)/Вход ЭКС'] #Вводим наименования столбцов
    price_df_sale.columns = cols
    roznitsa_list_sale = []
    for i in range(len(price_df_sale)):
        roznitsa_list_sale.append(round(price_df_sale.iloc[i,3]* 1.5+0.5, 0)) #'Базовый(РФ)/Вход ЭКС'*1.5 +0.5 для округления в большую сторону
    price_df_sale['Розница ЭКС'] = roznitsa_list_sale    
    return price_df_sale

#Мой прайс-лист, выгрузка
def def_price_my_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts):
    name_sheets_my = {todays_date: price_my_to_xlsx, todays_date+'(Р)': price_public_sale_to_xlsx}
    writer_my = pd.ExcelWriter(file_directory_resalts+'Прайс-лист_СТ_'+todays_date+'_мой.xlsx', engine='xlsxwriter')
    for sheet_name in name_sheets_my.keys():
        name_sheets_my[sheet_name].to_excel(writer_my, sheet_name=sheet_name, index=False)
    sheet_0 = writer_my.sheets[todays_date]
    sheet_0.set_column(0, 0, 50)
    sheet_0.set_column(1, 1, 11)
    sheet_0.set_column(2, 2, 8)
    sheet_0.set_column('D:H', 12)

    sheet_1 = writer_my.sheets[todays_date+'(Р)']
    sheet_1.set_column(0, 0, 50)
    sheet_1.set_column(1, 1, 11)
    sheet_1.set_column(2, 2, 8)
    sheet_1.set_column('D:E', 22)
    writer_my.save()

#Публичный прайс-лист, выгрузка
def def_price_public_basic_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts):
    price_public_basic_to_xlsx = price_my_to_xlsx.drop('% скидки ЭКС', axis=1)
    name_sheets_public = {todays_date: price_public_basic_to_xlsx, 'Распродажа': price_public_sale_to_xlsx}
    writer_public = pd.ExcelWriter(file_directory_resalts+'Прайс-лист_СТ_'+todays_date+'_(с распродажей).xlsx', engine='xlsxwriter')
    for sheet_name in name_sheets_public.keys():
        name_sheets_public[sheet_name].to_excel(writer_public, sheet_name=sheet_name, index=False)
    sheet_0 = writer_public.sheets[todays_date]
    sheet_0.set_column(0, 0, 50)
    sheet_0.set_column(1, 1, 11)
    sheet_0.set_column(2, 2, 8)
    sheet_0.set_column('D:G', 12)

    sheet_1 = writer_public.sheets['Распродажа']
    sheet_1.set_column(0, 0, 50)
    sheet_1.set_column(1, 1, 11)
    sheet_1.set_column(2, 2, 8)
    sheet_1.set_column('D:E', 22)
    writer_public.save()    