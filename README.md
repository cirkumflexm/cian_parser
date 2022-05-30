Краулер и парсер для сайта cian.ru
Сделано на Scrapy 2.6
Для запуска краулера необходимо перейти в папку /cian и запустить сбор данных командой 

scrapy crawl cian

Запуска краулера без вывода информации о работе с ключем --nolog 

scrapy crawl cian --nolog 

Для вывода результатов парсинга в файла запуск с ключем -o

scrapy crawl cian --nolog -o result.jl

Форматы вывода в соответствии с документацией https://docs.scrapy.org/en/latest/topics/feed-exports.html

Циан блокирует частые запросы с одного IP адреса, поэтому в краулере предусмотренная настройка прокси.
Для того чтобы запросы производились через прокси необходимо в файле cian/cian/local_settings.py указать настройки в следующем формате

proxy = 'https://login:password@IP:PORT'