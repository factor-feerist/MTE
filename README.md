# MTE
Многопользовательский редактор. Авторы: Сыч Эрнест, Куксовский Илья
## Запуск
Для подключения пользователей должен быть запущен файл server/server.py
Работа пользователей осуществляется через консоль, для запуска просто откройте файл client/shell.py
## Набор команд
### ?
    > ?
    Выдает список доступных команд
### help
    > help = ?
    > help 'команда'
    выдаст подсказку по использованию команды
### login
    > login 'имя пользователя'
    инициализирует пользователя для дальнейшей работы
### logout
    > logout
    закрывает сессию пользователя
### new
    > new 'название файла'
    создает новый файл для многопользовательского редактирования
### open
    > open 'название файла'
    открывает существующий файл для многопользовательского редактирования
### watch
    > watch 'название файла' 'версия файла'
    > watch 'название файла' = watch 'название файла' actual
    просматривает какую-либо версию файла на сервере, не отправляя на него изменений
### log
    > log 'название файла'
    просматривает историю изменений файла
## Работа с файлами
Для каждого файла на сервере есть актуальная версия, которая сохраняется даже если закрыть окно редактора на крестик и выйти из shell.py (обновления актуальной версии происходят по изменению текста после команды new или open)
Нажатие Save в окне текстового редактора приведет к сохранению версии файла под очередным номером, далее эту версию можно будет посмотреть с помощью команды watch, но изменения не будут отправляться на сервер