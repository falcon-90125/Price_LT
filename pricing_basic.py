#Файл ценообразования для закачки в базу по основным позициям
'''Т.к. в базе есть позиции с артикулами-дублями, которых в прайсе уже нет, но цены нужно по ним актуализировать(возможно ещё есть остатки по ним),
то сначала выявляем эти дубли - Мёрджим файл дублей и Прайс-лист СТ, затем объединяем основной прайс-лист и фрагмент прайса с Артикулами-дублями'''
#библиотеки
import pandas as pd

def def_pricing_basic(prices_in_vesta, art_dubl_df, prices_LT, file_directory_prices_in_vesta, todays_date):
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
    # prices_LT_concat.to_excel(file_directory_prices_in_vesta + 'Файл ЦО промежуточный_basic.xlsx')

    # Мёрджим prices_LT_concat и файл из карточки ценообразования
    prices_LT_merge = prices_LT_concat.merge(prices_in_vesta, on='Артикул', how='left')
    prices_LT_merge = prices_LT_merge.dropna(axis=0, how='any') #Удаляем строки с NaN
    prices_LT_merge.reset_index(inplace=True) # Обновляем индексы
    prices_LT_merge = prices_LT_merge.drop('index', axis=1) # Удаляем старые индексы
    print('Актуальных позиций по прайсу_basis: ', len(prices_LT_merge))
    # Если есть расхождения в ценах: Базовый(РФ)-ТарифПост валюта, МРЦ-МРЦ база, Вход ЭКС-Актуальная для транзитов, Розница ЭКС-Розница
    # то ставим метку 1 по данной позиции - собираем список с метками, затем передаём его в новый крайний столбец 'change'
    change_list = []
    for i in range(len(prices_LT_merge)):
        if prices_LT_merge.iloc[i,3] != prices_LT_merge.iloc[i,9] or prices_LT_merge.iloc[i,4] != prices_LT_merge.iloc[i,11] \
            or prices_LT_merge.iloc[i,6] != prices_LT_merge.iloc[i,12] or prices_LT_merge.iloc[i,7]/prices_LT_merge.iloc[i,10] > 1.01 \
                or prices_LT_merge.iloc[i,7]/prices_LT_merge.iloc[i,10] < 0.99 :
            change_list.append('1')
        else:
            change_list.append('0')
    prices_LT_merge['change'] = change_list #добавляем колонку с метками 0 и 1 списка change_list

    nomenclature_change = prices_LT_merge[prices_LT_merge.change == '1'] #отбираем только с "1", т.е. те, по которым есть изменения цен
    print('Количество позиций подлежащих изменению_basis:', len(nomenclature_change))
    # Выгрузка для визуальной проверки подлежащих изменению позиций
    if len(nomenclature_change) > 0:
        nomenclature_change.to_excel(file_directory_prices_in_vesta + 'Отчёт по изменениям_basis_' + todays_date + '.xlsx')

    nomenclature_change.rename(columns={'Код': 'IDNomenkl', 'Базовый(РФ)': 'Cena', '% скидки ЭКС': 'ProcentSkidki'}, inplace=True) # переименовываем столбцы для загрузочного файла
    nomenclature_change['TorgNacen'] = (nomenclature_change.loc[:, 'Розница ЭКС'] / nomenclature_change.loc[:, 'Вход ЭКС']-1)*100
    nomenclature_change['ProcentMinNacen'] = round((1-nomenclature_change['МРЦ'] / nomenclature_change['Cena'])*100, 5)
    nomenclature_change['Transport'] = 0
    nomenclature_change['StepenRound'] = 0
    nomenclature_change.drop(nomenclature_change.columns[[0, 1, 2, 4, 6, 7, 9, 10, 11, 12, 13]], axis='columns', inplace=True)
    nomenclature_change = nomenclature_change[['IDNomenkl', 'Cena', 'ProcentSkidki', 'TorgNacen', 'ProcentMinNacen', 'Transport', 'StepenRound']]
    nomenclature_change = nomenclature_change.sort_values('IDNomenkl')
    return nomenclature_change