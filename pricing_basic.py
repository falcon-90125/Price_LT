#Файл ценообразования для закачки в базу по основным позициям
'''Т.к. в базе есть позиции с артикулами-дублями, которых в прайсе уже нет, но цены нужно по ним актуализировать(возможно ещё есть остатки по ним),
то сначала выявляем эти дубли - Мёрджим файл дублей и Прайс-лист СТ, затем объединяем основной прайс-лист и фрагмент прайса с Артикулами-дублями'''
#библиотеки
import pandas as pd
import numpy as np

def def_pricing_basic(prices_in_vesta, art_dubl_df, prices_LT, file_directory_output):
    prices_LT = prices_LT.dropna(axis=0, how='any') #удаляем строки "Ценовая группа" с пустыми ячейками в ценах

    # Мёрджим файл дублей и Прайс-лист СТ, чтобы взять цены по дублям
    prices_LT_merge_art_dubl = art_dubl_df.merge(prices_LT, on='Артикул', how='left')
    prices_LT_merge_art_dubl = prices_LT_merge_art_dubl.dropna(axis=0, how='any') #Удаляем строки с NaN
    prices_LT_merge_art_dubl.drop('Артикул', axis=1, inplace=True) #Удаляем столбец 'Артикул' по прайсу

    #Перемещаем столбец 'Артикул_дубль' туда же как в прайс-листе
    prices_LT_art_dubl = prices_LT_merge_art_dubl[['Наименование','Артикул_дубль','Ед. изм.','Базовый (РФ)','МРЦ','Скидка ЭКС', 'Вход ЭКС', 'Розница ЭКС']]
    prices_LT_art_dubl.rename(columns={'Артикул_дубль': 'Артикул'}, inplace=True) # переименовываем столбец'Артикул_дубль' на 'Артикул'
    prices_LT_concat = pd.concat([prices_LT, prices_LT_art_dubl]) # Объединяем прайс-лист и фрагмент прайса с Артикулами-дублями
    prices_LT_concat.reset_index(inplace=True) # Обновляем индексы
    prices_LT_concat = prices_LT_concat.drop('index', axis=1) # Удаляем старые индексы
    # Выгрузка для визуальной проверки конкатенации
    # prices_LT_concat.to_excel(file_directory_ouput + 'Файл ЦО промежуточный_basic.xlsx')

    #Обрабатываем файл из карточки ценообразования - prices_in_vesta
    prices_in_vesta = prices_in_vesta.dropna(subset=['Артикул']) # Удаляем строки c Nan в столбце 'Артикул', они бесполезны
    #Удаляем строки содержащие в артикулах 'обр' и 'бр', тоже бесполезны    
    prices_in_vesta = prices_in_vesta.drop(prices_in_vesta[prices_in_vesta['Артикул'].str.contains('обр')].index)
    prices_in_vesta = prices_in_vesta.drop(prices_in_vesta[prices_in_vesta['Артикул'].str.contains('бр')].index)
    #Переименовать столбец 'МРЦ' в 'МРЦ база', чтобы не было путаницы в дальнейшей обработке после мёрджа
    prices_in_vesta.rename(columns={'МРЦ': 'МРЦ база'}, inplace=True)
    #Меняем тип данных в столбце 'Артикул' на np.int64, т.к. в исходном файле - "str"    
    prices_in_vesta['Артикул'] = prices_in_vesta['Артикул'].astype(np.int64)
    #Округляем цены, т.к. в исходном файле 3-4 знака после запятой    
    prices_in_vesta['Актуальная для транзитов'] = round(prices_in_vesta['Актуальная для транзитов'], 2)

    #Мёрджим prices_LT_concat и prices_in_vesta
    prices_LT_merge = prices_LT_concat.merge(prices_in_vesta, on='Артикул', how='left')
    prices_LT_merge = prices_LT_merge.dropna(axis=0, how='any') #Удаляем строки с NaN, они бесполезны
    prices_LT_merge.reset_index(inplace=True) # Обновляем индексы
    prices_LT_merge = prices_LT_merge.drop('index', axis=1) # Удаляем старые индексы
    print('Актуальных позиций по прайсу_basis: ', len(prices_LT_merge))# Принтим сколько позиций в базе соответствует прайсу

    # Проверяем расхождения в ценах в прайсе и в базе, формируем файл ценообразования по позициям с расхождениями
    # Если есть расхождения в ценах: Базовый(РФ)/ТарифПост валюта., МРЦ/МРЦ база, Вход ЭКС/Актуальная для транзитов, Розница ЭКС/Розница
    # то ставим метку 1 по данной позиции - собираем список с метками, затем передаём его в новый крайний столбец 'change'
    change_list = []
    for i in range(len(prices_LT_merge)):
        if (abs(prices_LT_merge.iloc[i,3] - prices_LT_merge.iloc[i,9]) / prices_LT_merge.iloc[i,9])*100 > 0.1 or \
            (abs(prices_LT_merge.iloc[i,4] - prices_LT_merge.iloc[i,11]) / prices_LT_merge.iloc[i,11])*100 > 0.1 or \
            (abs(prices_LT_merge.iloc[i,6] - prices_LT_merge.iloc[i,12]) / prices_LT_merge.iloc[i,12])*100 > 0.1 or \
            ((abs(prices_LT_merge.iloc[i,7] - prices_LT_merge.iloc[i,10]) / prices_LT_merge.iloc[i,10])*100 > 0.1 and prices_LT_merge.iloc[i,3] > 999.99):        
            change_list.append('1')
        else:
            change_list.append('0')
    prices_LT_merge['change'] = change_list #добавляем колонку с метками 0 и 1 списка change_list

    # Отбираем строки в меткой "1", т.е. те, по которым есть изменения цен
    nomenclature_change = prices_LT_merge[prices_LT_merge.change == '1']
    print('Количество позиций подлежащих изменению_basis:', len(nomenclature_change))# Принтим сколько позиций подлежат изменению

    # Формирование и выгрузка файла для визуальной проверки подлежащих изменению позиций
    if len(nomenclature_change) > 0:
        nomenclature_change_to_excel = nomenclature_change.iloc[:, [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]] #Формируем новый df без '% скидки ЭКС' и 'change'
        #Назначаем новый порядок столбцов
        columns_nomenclature_change_to_excel=['Код', 'Наименование', 'Артикул', 'Ед. изм.', 'Базовый (РФ)', 'ТарифПост валюта.', 'МРЦ', 'МРЦ база', 'Вход ЭКС', 'Актуальная для транзитов', 'Розница ЭКС', 'Розница']
        nomenclature_change_to_excel = nomenclature_change_to_excel.reindex(columns=columns_nomenclature_change_to_excel)
        #Сортируем по 'Код'
        nomenclature_change_to_excel = nomenclature_change_to_excel.sort_values('Код')
        #Выгружаем файл
        nomenclature_change_to_excel.to_excel(file_directory_output + 'Oтчёт по изменениям базовый.xlsx', index=False)

    #Формируем файл ценообразования и выгружаем в output
    nomenclature_change.rename(columns={'Код': 'IDNomenkl', 'Базовый (РФ)': 'Cena', 'Скидка ЭКС': 'ProcentSkidki'}, inplace=True) # переименовываем столбцы для загрузочного файла
    nomenclature_change['TorgNacen'] = (nomenclature_change.loc[:, 'Розница ЭКС'] / nomenclature_change.loc[:, 'Вход ЭКС']-1)*100
    nomenclature_change['ProcentMinNacen'] = round((1-nomenclature_change['МРЦ'] / nomenclature_change['Cena'])*100, 5)
    nomenclature_change['Transport'] = 0
    nomenclature_change['StepenRound'] = 0
    nomenclature_change.drop(nomenclature_change.columns[[0, 1, 2, 4, 6, 7, 9, 10, 11, 12, 13]], axis='columns', inplace=True)
    nomenclature_change = nomenclature_change[['IDNomenkl', 'Cena', 'ProcentSkidki', 'TorgNacen', 'ProcentMinNacen', 'Transport', 'StepenRound']]
    nomenclature_change = nomenclature_change.sort_values('IDNomenkl')
    nomenclature_change.to_excel(file_directory_output + 'Закачка Световые Технологии база.xlsx', sheet_name='ActualCeni', index=False)