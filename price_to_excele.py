# Выгрузка прайс-листов

# библиотеки
import pandas as pd

#Мой прайс-лист, выгрузка
def def_price_my_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts, file_name_price_LT):
    name_sheets_my = {todays_date: price_my_to_xlsx, todays_date+'(Р)': price_public_sale_to_xlsx}
    writer_my = pd.ExcelWriter(file_directory_resalts+file_name_price_LT, engine='xlsxwriter') #'Прайс-лист_СТ_'+todays_date+'_мой.xlsx'
    workbook_my = writer_my.book #записываем объект 'xlsxwriter' в книгу, для последующих назначений форматов
    format1 = workbook_my.add_format({'num_format': '#,##0.00'})
    format_art = workbook_my.add_format({'num_format': '#,##0.00'})
    for sheet_name in name_sheets_my.keys():
        name_sheets_my[sheet_name].to_excel(writer_my, sheet_name=sheet_name, index=False)
    sheet_0 = writer_my.sheets[todays_date]
    sheet_0.set_column(0, 0, 50)
    sheet_0.set_column('B:C', 11, format_art)
    sheet_0.set_column(2, 2, 8)
    sheet_0.set_column('D:H', 12, format1)

    sheet_1 = writer_my.sheets[todays_date+'(Р)']
    sheet_1.set_column(0, 0, 50)
    sheet_1.set_column(1, 1, 11, format_art)
    sheet_1.set_column(2, 2, 8)
    sheet_1.set_column('D:E', 22, format1)
    writer_my._save() #для запуска в контейнере
    # writer_my.save() #для запуска кода

#Публичный прайс-лист, выгрузка
def def_price_public_basic_to_xlsx(price_my_to_xlsx, price_public_sale_to_xlsx, todays_date, file_directory_resalts):
    price_public_basic_to_xlsx = price_my_to_xlsx.drop('Скидка ЭКС', axis=1)
    name_sheets_public = {todays_date: price_public_basic_to_xlsx, 'Распродажа': price_public_sale_to_xlsx}
    writer_public = pd.ExcelWriter(file_directory_resalts+'Прайс-лист_СТ_'+todays_date+'_(с распродажей).xlsx', engine='xlsxwriter')
    workbook_public = writer_public.book #записываем объект 'xlsxwriter' в книгу, для последующих назначений форматов
    format1 = workbook_public.add_format({'num_format': '#,##0.00'})
    format_art = workbook_public.add_format({'num_format': '0.'})
    for sheet_name in name_sheets_public.keys():
        name_sheets_public[sheet_name].to_excel(writer_public, sheet_name=sheet_name, index=False)
    sheet_0 = writer_public.sheets[todays_date]
    sheet_0.set_column(0, 0, 50)
    sheet_0.set_column(1, 1, 11, format_art)
    sheet_0.set_column(2, 2, 8)
    sheet_0.set_column('D:G', 12, format1)

    sheet_1 = writer_public.sheets['Распродажа']
    sheet_1.set_column(0, 0, 50)
    sheet_1.set_column(1, 1, 11, format_art)
    sheet_1.set_column(2, 2, 8)
    sheet_1.set_column('D:E', 22, format1)
    writer_public._save() #для запуска в контейнере
    # writer_public.save() #для запуска кода

#Прайс в закрома
def def_to_zakroma(price_my_to_xlsx, price_public_sale_to_xlsx, file_name_price_to_zakroma, file_directory_output, todays_date):
    price_to_zakroma = price_my_to_xlsx.drop(price_my_to_xlsx.columns[[5]], axis='columns')
    price_sale = price_public_sale_to_xlsx.dropna(axis=0)
    price_sale.rename(columns={'Базовый(РФ)/Вход ЭКС': 'Базовый (РФ)'}, inplace=True)
    price_sale['МРЦ'] = price_sale['Базовый (РФ)'].apply(lambda x: round(x * 1.15 + 0.5, 0))
    price_sale['Вход ЭКС'] = price_sale['Базовый (РФ)']
    price_sale = price_sale[['Наименование', 'Артикул', 'Ед. изм.', 'Базовый (РФ)', 'МРЦ', 'Вход ЭКС', 'Розница ЭКС']]
    price_to_zakroma = pd.concat([price_to_zakroma, price_sale])
    price_to_zakroma.to_excel(file_directory_output + file_name_price_to_zakroma + todays_date +'.xlsx', index=False)

    #Прайс в закрома с дублями
def def_to_zakroma_dubl(file_directory_input, file_name_art_dubl, file_directory_output, file_name_price_to_zakroma, todays_date):
    price_to_zakroma = pd.read_excel(file_directory_output+file_name_price_to_zakroma+todays_date +'.xlsx')
    art_dubl_df = pd.read_excel(file_directory_input+file_name_art_dubl)
    art_dubl_merge_df = art_dubl_df.merge(price_to_zakroma, on='Артикул', how='left')
    art_dubl_merge_df = art_dubl_merge_df.dropna()
    art_dubl_merge_df = art_dubl_merge_df.drop('Артикул', axis=1)
    art_dubl_merge_df.rename(columns={'Артикул_дубль': 'Артикул'}, inplace=True)
    art_dubl_merge_df = art_dubl_merge_df.reindex(columns=['Наименование', 'Артикул', 'Ед. изм.', 'Базовый (РФ)', 'МРЦ', 'Вход ЭКС', 'Розница ЭКС'])
    price_to_zakroma = pd.concat([price_to_zakroma, art_dubl_merge_df])

    price_to_zakroma.to_excel(file_directory_output + file_name_price_to_zakroma + todays_date +'.xlsx', index=False)