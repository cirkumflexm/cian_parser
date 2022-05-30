Краулер и парсер для сайта cian.ru
Сделано на Scrapy 2.6
Для запуска краулера необходимо перейти в папку /cian и запустить сбор данных командой 
scrapy crawl cian

Запуска краулера без вывода информации о работе с ключем --nolog 
scrapy crawl cian --nolog 

Для вывода результатов парсинга в файла запуск с ключем -o
scrapy crawl cian --nolog -o result.jl

Форматы вывода в соответствии с документацией https://docs.scrapy.org/en/latest/topics/feed-exports.html