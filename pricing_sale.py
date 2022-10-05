#Файл ценообразования для закачки в базу
'''Т.к. в базе есть позиции с артикулами-дублями, которых в прайсе уже нет, но цены нужно по ним актуализировать(возможно ещё есть остатки по ним),
то сначала выявляем эти дубли - Мёрджим файл дублей и Прайс-лист СТ, затем объединяем основной прайс-лист и фрагмент прайса с Артикулами-дублями'''
#библиотеки
import pandas as pd
# todays_date = '2022-09-30'

# # #Директории для прайс-листов
# file_directory_resalts = 'E:\Соколов Алексей\Documents\ПОСТАВЩИКИ I\СВЕТОВЫЕ ТЕХНОЛОГИИ\Прайс-листы Световые технологии/'
# # file_name = todays_date+'_Прайс_CТ.xlsx'
# # file_name_sale = todays_date+'_Прайс_CТ_распродажа.xlsx'
# file_name_price_LT = 'Прайс-лист_СТ_'+todays_date+'_мой.xlsx'

# #Директории для файлов ценообразования
# file_directory_prices_in_vesta = 'E:\Соколов Алексей\Documents\Номенклатура\Цены\Световые Технологии/'
# file_name_prices = 'Цены_СТ_'+todays_date+'.xlsx' #Выгрузить из карточки ценообразования по Поставщику МГК Световые Технологии ООО, код 81948
# file_name_art_dubl = 'Артикул_дубль.xlsx'
# prices_in_vesta = pd.read_excel(file_directory_prices_in_vesta+file_name_prices)

# #Загружаем Прайс-лист_СТ_todays_date_мой, типа Прайс-лист_СТ_2022-09-12_мой
# prices_LT_sale = pd.read_excel(file_directory_resalts+file_name_price_LT, sheet_name=todays_date+'(Р)')
# #Загружаем файл дублей
# art_dubl_df = pd.read_excel(file_directory_prices_in_vesta+file_name_art_dubl)

def def_pricing_sale(prices_in_vesta, art_dubl_df, prices_LT_sale):
    # prices_in_vesta.drop(prices_in_vesta.columns[[0, 1, 3, 5, 6, 7, 8,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,32]], axis='columns', inplace=True)
    prices_LT_sale = prices_LT_sale.dropna(axis=0, how='any') #удаляем строки "Ценовая группа" с пустыми ячейками в ценах

    # Мёрджим файл дублей и Прайс-лист СТ, чтобы взять цены по дублям
    prices_LT_merge_art_dubl = art_dubl_df.merge(prices_LT_sale, on='Артикул', how='left')
    prices_LT_merge_art_dubl = prices_LT_merge_art_dubl.dropna(axis=0, how='any') #Удаляем строки с NaN
    prices_LT_merge_art_dubl.drop('Артикул', axis=1, inplace=True) #Удаляем столбец 'Артикул' по прайсу

    # Перемещаем столбец 'Артикул_дубль' туда же как в прайс-листе
    prices_LT_art_dubl = prices_LT_merge_art_dubl[['Номенклатура','Артикул_дубль','Ед. изм.','Базовый(РФ)/Вход ЭКС', 'Розница ЭКС']]
    prices_LT_art_dubl.rename(columns={'Артикул_дубль': 'Артикул'}, inplace=True) # переименовываем стодбец'Артикул_дубль' на 'Артикул'
    prices_LT_concat = pd.concat([prices_LT_sale, prices_LT_art_dubl]) # Объединяем прайс-лист и фрагмент прайса с Артикулами-дублями
    prices_LT_concat.reset_index(inplace=True) # Обновляем индексы
    prices_LT_concat = prices_LT_concat.drop('index', axis=1) # Удаляем старые индексы
    # Выгрузка для визуальной проверки конкатенации
    # prices_LT_concat.to_excel(file_directory_prices_in_vesta + 'Файл ЦО промежуточный.xlsx')

    # Мёрджим prices_LT_concat и файл из карточки ценообразования
    prices_LT_merge = prices_LT_concat.merge(prices_in_vesta, on='Артикул', how='left')
    prices_LT_merge = prices_LT_merge.dropna(axis=0, how='any') #Удаляем строки с NaN
    prices_LT_merge.reset_index(inplace=True) # Обновляем индексы
    prices_LT_merge = prices_LT_merge.drop('index', axis=1) # Удаляем старые индексы
    print('Актуальных позиций по прайсу: ', len(prices_LT_merge))

    # Если есть расхождения в ценах: Базовый(РФ)-Уч.цена вал., МРЦ-МРЦ база, Вход ЭКС-Актуальная для транзитов, Розница ЭКС-Розница
    # то ставим метку 1 по данной позиции - собираем список с метками, затем передаём его в новый крайний столбец 'change'
    change_list = []
    for i in range(len(prices_LT_merge)):
        if prices_LT_merge.iloc[i,3] != prices_LT_merge.iloc[i,6] or prices_LT_merge.iloc[i,4] != prices_LT_merge.iloc[i,7]:
            change_list.append('1')
        else:
            change_list.append('0')
    prices_LT_merge['change'] = change_list

    nomenclature_change = prices_LT_merge[prices_LT_merge.change == '1']
    print('Количество позиций подлежащих изменению:', len(nomenclature_change))
    # Выгрузка для визуальной проверки подлежащих изменению позиций
    # nomenclature_change.to_excel(file_directory_prices_in_vesta + 'Файл ЦО промежуточный.xlsx')

    nomenclature_change.rename(columns={'Код': 'IDNomenkl', 'Базовый(РФ)/Вход ЭКС': 'Cena'}, inplace=True) # переименовываем столбцы для загрузочного файла
    nomenclature_change['ProcentSkidki'] = 0
    nomenclature_change['TorgNacen'] = (nomenclature_change['Розница ЭКС'] / nomenclature_change['Cena']-1)*100
    nomenclature_change['ProcentMinNacen'] = -15
    nomenclature_change['Transport'] = 0
    nomenclature_change['StepenRound'] = 0
    nomenclature_change.drop(nomenclature_change.columns[[0, 1, 2, 4, 6, 7, 8, 9, 10]], axis='columns', inplace=True)
    nomenclature_change = nomenclature_change[['IDNomenkl', 'Cena', 'ProcentSkidki', 'TorgNacen', 'ProcentMinNacen', 'Transport', 'StepenRound']]
    nomenclature_change_sale = nomenclature_change.sort_values('IDNomenkl')
    return nomenclature_change_sale

# print(nomenclature_change_sale.head(5))
# nomenclature_change.to_excel(file_directory_prices_in_vesta + 'Закачка Световые Технологии' + file_name_prices[7:-5] +'_sale.xlsx', sheet_name='ActualCeni', index=False)