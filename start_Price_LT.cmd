# Сборка образа
# docker build . -t price_lt:date

# Сборка контейнера
# docker create --name price_lt -v C:/Users/sokolov/Yandex_Disk/MyData/Projects/Price_LT/exchange:/app/exchange price_lt:date

# Запуск контейнера
docker start price_lt