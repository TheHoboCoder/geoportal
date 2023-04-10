# Описание
## Введение

Данный проект - веб-ГИС на базе фреймворка GeoDjango, которая предоставляет
платформу для установки и работы геомодулей. Главной целью проекта
является упрощение публикации алгоритмов по обработке пространственных данных.

Стек проекта:

*бэкенд*:
GeoDjango
PostgreSQL+PostGIS

*фронтенд*:
OpenLayers
*Vue.js* (в процессе перехода, пока jquery)


## Функционал

Административная панель django позволяет создателям модулей и администраторам сайта загружать и удалять модули, а также работать со связанными с ними данными: слоями и пространственными данными.

Главная страница сайта представляет собой интерактивную карту, на которой можно
выбрать модуль из списка. После загрузки модуля отображается список его слоев.

## Установка

### bash
### docker

## Разработчикам модулей

# Структура проекта

Директории geoportal_core и geoportal содержат основной код проекта.
Любые классы и функции, опредленные в этих директориях, предназначены только для 
внутреннего использования. Модуль не должен содержать импортов из них.

Директория common предоставляет API для работы модуля и служит связующим звеном между
модулем и геопорталом. 

# Пример модуля

В папке sample_module находится пример модуля.

Модуль обязательно должен содержать module_config с описанием конфигурации.
В этом файле должны быть определены переменные COMMANDS типа CommandList, и SCHEMA типа Schema.

# Описание команд

Для создания команды необходимо определить сериализатор с описанием входных данных 
для команды и создать класс команды, наследующий от CommandView. 
Затем добавить команду в COMMANDS.

Алгоритм работы:
- сериализатор используется для отрисовки формы для команды на сайте
- при отправке формы на сервере происходит валидация данных с помощью сериализатора
- проверенные данные передаются в обработчик команды
- обработчик должен вернуть CommandResponse
- CommandResponse отрисовывается на карте

## Создание сериализатора для команды

По соглашению Django сериализаторы определяются в файле serializers.py.
Сериализатор описывает данные, а также алгоритмы их валидации.
Более подробно про поля сериализатора и валидацию можно почитать здесь:
https://www.django-rest-framework.org/api-guide/serializers/

## Создание сериализатора для команды

Так как команда является представлением, то ее можно определять в файле views.py
Команды должны наследовать класс CommandResponse. В нем нужно определить handler, 
который принимает словарь с данными и возвращает CommandResponse. (см. common/commands/CommandResponse)







