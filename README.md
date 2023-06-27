Результат работы программы: обработка прайс-листов "Световые технологии" и формирование прайсов собстветнного формата (1 - для себя и 2 - для менеджеров):

папка exchange\output:

1. Прайс-лист_СТ_2023-05-02_мой.xlsx

2. Прайс-лист_СТ_2023-05-02_(с распродажей).xlsx

Формирование файлов для загрузки в документ ценообразования в Весте:

- Закачка Световые Технологии база.xlsx

- Закачка Световые Технологии распродажа.xlsx

Формирование файлов-отчётов с позицими подлежащих изменению цен для визуальной проверки

- Oтчёт по изменениям базовый.xlsx

- Oтчёт по изменениям распродажа.xlsx

Формирование файла с ценами "в закрома" для отображения цен позиций отстутствующих в БД
- Прайс Световые технологии с распродажей - в закрома.xlsx

Поместить на W:\Документы_Общие\Остатки поставщиков\ВД\81948 Световые технологии\Цены

Трубуемые файлы на вход программы, папка exchange\input:

- data_price.txt - указать в нём дату, которая будет указана в прайс-листе(часто прайсы делаются заранее).

- Артикул_дубль.xlsx - Т.к. в базе есть позиции с артикулами-дублями, которых в прайсе уже нет, 
но цены нужно по ним актуализировать(возможно ещё есть остатки по ним).

- Прайс_CТ.xlsx - прайс "Световые технологии" из личного кабинета на сайте "СТ"

- Прайс_CТ_распродажа.xlsx - прайс "Световые технологии" из личного кабинета на сайте "СТ"

- Цены_СТ_из_Весты.xlsx - файл выгрузки актуальных цен из БД, документ ценообразования по Поставщику МГК Световые Технологии ООО, код 81948

start_Price_LT - файл запуска Docker-контейнера