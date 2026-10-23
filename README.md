## Управление таблицами

Запуск: `database`

Команды:
- `create_table <имя> <столбец:тип> ...` — создать таблицу (типы: int, str, bool)
- `drop_table <имя>` — удалить таблицу
- `list_tables` — показать все таблицы
- `help` — справка
- `exit` — выход

Пример:

```
>>>Введите команду: create_table users name:str age:int
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int
>>>Введите команду: list_tables
- users
```
## Демонстрация

[Видео-демонстрация работы пакета](https://drive.google.com/file/d/1cVKkf2GoYBZ7X8Z8kSMc-1cI97Sle5r-/view?usp=sharing)

[Видео-демонстрация CRUD-операций](https://drive.google.com/file/d/1RPYWBjNLuxHFOwEGyDAOUSLTn8o4ho0D/view?usp=sharing)

## CRUD-операции

Команды для работы с данными (строки пишутся в двойных кавычках):

- `insert into <таблица> values (<значение1>, <значение2>, ...)` — добавить запись (ID создаётся автоматически)
- `select from <таблица>` — показать все записи
- `select from <таблица> where <столбец> = <значение>` — показать записи по условию
- `update <таблица> set <столбец> = <значение> where <столбец> = <значение>` — обновить записи
- `delete from <таблица> where <столбец> = <значение>` — удалить записи
- `info <таблица>` — информация о таблице

Пример:

```
>>>Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".
>>>Введите команду: select from users where age = 28
```