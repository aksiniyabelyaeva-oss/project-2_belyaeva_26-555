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