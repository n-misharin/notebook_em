# Реализация

### Использовано

Приложение было написано на `python 3.9`.

Из сторонних библиотек используется только библиотека `phonenumber`.

### Перед запуском

`> pip install requirements.txt`

### Запуск
`> python main.py`

## Описание

Чтобы взаимодействовать с приложением (после запуска)
нужно вводить команды в консоль. Можно ввести `help`,
чтобы получить список доступных команд.

В приложении можно:
1) добавлять записи в справочник
2) выводить данные в консоль постранично (10 записей на странице)
3) редактировать записи
4) удалять записи
5) искать записи по нескольким характеристикам

Поиск производится линейно. Если вводится id записи, то ищется запись, которая
имеет id равное введенному. Если поиск осуществляется по другим характеристикам,
то ищется наличие введенной подстроки в значении соответствующего поля. В итоговой
выборке окажутся только те записи из таблицы, у которых во всех полях были найдены
вхождения шаблона поиска.

Данные приложения хранятся в файле `data/db`. После запуска
приложения, в папке `data` появиться файл `.db`. Это файл для
временного хранения данных.
## Задание

Реализовать телефонный справочник со следующими возможностями:
1. Вывод постранично записей из справочника на экран
2. Добавление новой записи в справочник
3. Возможность редактирования записей в справочнике
4. Поиск записей по одной или нескольким характеристикам

Требования к программе:
1. Реализация интерфейса через консоль (без веб- или графического интерфейса)
2. Хранение данных должно быть организовано в виде текстового файла, формат которого придумывает сам программист
3. В справочнике хранится следующая информация: фамилия, имя, отчество, название организации, телефон рабочий, телефон личный (сотовый)

Плюсом будет:
1) аннотирование функций и переменных
2) документирование функций
3) подробно описанный функционал программы
4) размещение готовой программы и примера файла с данными на github
