#библиотеки
import pandas as pd

columns = ['country', 'province', 'region_1', 'region_2'] # Создаем список, в котором будут храниться названия столбцов
index = [0, 1, 10, 100] # Создаем список, в котором будут индексы строк

# Создаем список с данными, каждая строка таблицы - отдельный список
data = [['Italy', 'Sicily & Sardinia', 'Etna', 'NaN'], 
        ['Portugal', 'Douro', 'NaN', 'NaN'],
       ['US', 'California', 'Napa Valley', 'Napa'],
       ['US', 'New York', 'Finger Lakes', 'Finger Lakes']]
df = pd.DataFrame(data, columns = columns, index = index) # Создаем ДатаФрейм (в качестве параметров передаем называние столбцов, индексы и сами данные)
print(df.loc[0][0])