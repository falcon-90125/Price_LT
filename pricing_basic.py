#Файл ценообразования для закачки в базу
'''Т.к. в базе есть позиции с артикулами-дублями, которых в прайсе уже нет, но цены нужно по ним актуализировать(возможно ещё есть остатки по ним),
то сначала выявляем эти дубли - Мёрджим файл дублей и Прайс-лист СТ, затем объединяем основной прайс-лист и фрагмент прайса с Артикулами-дублями'''
#библиотеки
import pandas as pd
from openpyxl.styles.numbers import BUILTIN_FORMATS

def def_pricing_basic(prices_in_vesta, art_dubl_df, prices_LT):
    # prices_in_vesta.drop(prices_in_vesta.columns[[0, 1, 3, 5, 6, 7, 8,10,11,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,32]], axis='columns', inplace=True)
    prices_LT = prices_LT.dropna(axis=0, how='any') #удаляем строки "Ценовая группа" с пустыми ячейками в ценах

    # Мёрджим файл дублей и Прайс-лист СТ, чтобы взять цены по дублям
    prices_LT_merge_art_dubl = art_dubl_df.merge(prices_LT, on='Артикул', how='left')
    prices_LT_merge_art_dubl = prices_LT_merge_art_dubl.dropna(axis=0, how='any') #Удаляем строки с NaN
    prices_LT_merge_art_dubl.drop('Артикул', axis=1, inplace=True) #Удаляем столбец 'Артикул' по прайсу
    #Перемещаем столбец 'Артикул_дубль' туда же как в прайс-листе
    prices_LT_art_dubl = prices_LT_merge_art_dubl[['Номенклатура','Артикул_дубль','Ед. изм.','Базовый(РФ)','МРЦ','% скидки ЭКС', 'Вход ЭКС', 'Розница ЭКС']]
    prices_LT_art_dubl.rename(columns={'Артикул_дубль': 'Артикул'}, inplace=True) # переименовываем стодбец'Артикул_дубль' на 'Артикул'
    prices_LT_concat = pd.concat([prices_LT, prices_LT_art_dubl]) # Объединяем прайс-лист и фрагмент прайса с Артикулами-дублями
    prices_LT_concat.reset_index(inplace=True) # Обновляем индексы
    prices_LT_concat = prices_LT_concat.drop('index', axis=1) # Удаляем старые индексы
    # Выгрузка для визуальной проверки конкатенации
    # prices_LT_concat.to_excel(file_directory_prices_in_vesta + 'Прайс промежуточный.xlsx')

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
        if prices_LT_merge.iloc[i,3] != prices_LT_merge.iloc[i,9] or prices_LT_merge.iloc[i,4] != prices_LT_merge.iloc[i,11] \
            or prices_LT_merge.iloc[i,6] != prices_LT_merge.iloc[i,12] or (prices_LT_merge.iloc[i,7]/prices_LT_merge.iloc[i,10]) > 1.01 \
                or (prices_LT_merge.iloc[i,10]/prices_LT_merge.iloc[i,7]) < 0.99 :
            change_list.append('1')
        else:
            change_list.append('0')
    prices_LT_merge['change'] = change_list

    nomenclature_change = prices_LT_merge[prices_LT_merge.change == '1']
    print('Количество позиций подлежащих изменению:', len(nomenclature_change))
    # print(nomenclature_change.head(5))
    # Выгрузка для визуальной проверки подлежащих изменению позиций
    # nomenclature_change.to_excel(file_directory_prices_in_vesta + 'Прайс промежуточный.xlsx')

    nomenclature_change.rename(columns={'Код': 'IDNomenkl', 'Базовый(РФ)': 'Cena', '% скидки ЭКС': 'ProcentSkidki'}, inplace=True) # переименовываем столбцы для загрузочного файла
    nomenclature_change['TorgNacen'] = (nomenclature_change['Розница ЭКС'] / nomenclature_change['Вход ЭКС']-1)*100
    nomenclature_change['ProcentMinNacen'] = round((1-nomenclature_change['МРЦ'] / nomenclature_change['Cena'])*100, 5)
    nomenclature_change['Transport'] = 0
    nomenclature_change['StepenRound'] = 0
    nomenclature_change.drop(nomenclature_change.columns[[0, 1, 2, 4, 6, 7, 9, 10, 11, 12, 13]], axis='columns', inplace=True)
    nomenclature_change = nomenclature_change[['IDNomenkl', 'Cena', 'ProcentSkidki', 'TorgNacen', 'ProcentMinNacen', 'Transport', 'StepenRound']]
    nomenclature_change = nomenclature_change.sort_values('IDNomenkl')
    return nomenclature_change

# print(nomenclature_change.head(5))
# nomenclature_change.to_excel(file_directory_prices_in_vesta + 'Закачка Световые Технологии' + file_name_prices[7:-5] +'.xlsx', sheet_name='ActualCeni', index=False)