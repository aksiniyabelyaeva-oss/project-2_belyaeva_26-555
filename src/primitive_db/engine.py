import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    is_valid_type,
    select,
    update,
)
from primitive_db.decorators import create_cacher
from primitive_db.parser import parse_condition, parse_values
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

META_FILE = "db_meta.json"

MODIFYING_COMMANDS = ("create_table", "drop_table", "insert", "update", "delete")
cache_result = create_cacher()


def reset_cache():
    global cache_result
    cache_result = create_cacher()


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values (<значение1>, ...) - создать")
    print("<command> select from <имя_таблицы> [where <столбец> = <значение>] - читать")
    print("<command> update <имя_таблицы> set <столбец> = <значение> where ...")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить")
    print("<command> info <имя_таблицы> - информация о таблице")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def check_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return False
    return True


def check_clause(metadata, table_name, clause):
    schema = dict(column.split(":") for column in metadata[table_name])
    for column, value in clause.items():
        if column not in schema or not is_valid_type(value, schema[column]):
            raise ValueError(f"{column} = {value}")


def handle_insert(metadata, user_input):
    head, sep, values_text = user_input.partition(" values ")
    words = head.split()
    if not sep or len(words) != 3 or words[1] != "into":
        raise ValueError(user_input)
    table_name = words[2]
    if not check_table(metadata, table_name):
        return
    values = parse_values(values_text)
    table_data = load_table_data(table_name)
    count = len(table_data)
    table_data = insert(metadata, table_name, values, table_data)
    if len(table_data) > count:
        save_table_data(table_name, table_data)
        record_id = table_data[-1]["ID"]
        print(f'Запись с ID={record_id} успешно добавлена в таблицу "{table_name}".')


def handle_select(metadata, user_input):
    rest = user_input[len("select"):].strip()
    if not rest.startswith("from "):
        raise ValueError(user_input)
    table_name, _, condition = rest[len("from "):].partition(" where ")
    table_name = table_name.strip()
    if not check_table(metadata, table_name):
        return
    where_clause = None
    if condition:
        where_clause = parse_condition(condition)
        check_clause(metadata, table_name, where_clause)
    key = f"{table_name}:{where_clause}"
    rows = cache_result(
        key, lambda: select(load_table_data(table_name), where_clause)
    )
    if not rows:
        print("Записей не найдено.")
        return
    names = [column.split(":")[0] for column in metadata[table_name]]
    pretty = PrettyTable(names)
    for row in rows:
        pretty.add_row([row[name] for name in names])
    print(pretty)


def handle_update(metadata, user_input):
    rest = user_input[len("update"):].strip()
    table_name, sep_set, rest = rest.partition(" set ")
    set_text, sep_where, where_text = rest.partition(" where ")
    table_name = table_name.strip()
    if not sep_set or not sep_where:
        raise ValueError(user_input)
    if not check_table(metadata, table_name):
        return
    set_clause = {}
    for part in set_text.split(","):
        set_clause.update(parse_condition(part))
    where_clause = parse_condition(where_text)
    if "ID" in set_clause:
        raise ValueError("ID изменять нельзя")
    check_clause(metadata, table_name, set_clause)
    check_clause(metadata, table_name, where_clause)
    table_data = load_table_data(table_name)
    ids = [row["ID"] for row in select(table_data, where_clause)]
    if not ids:
        print("Записей не найдено.")
        return
    save_table_data(table_name, update(table_data, set_clause, where_clause))
    for record_id in ids:
        print(f'Запись с ID={record_id} в таблице "{table_name}" успешно обновлена.')


def handle_delete(metadata, user_input):
    rest = user_input[len("delete"):].strip()
    if not rest.startswith("from "):
        raise ValueError(user_input)
    table_name, sep, condition = rest[len("from "):].partition(" where ")
    table_name = table_name.strip()
    if not sep:
        raise ValueError(user_input)
    if not check_table(metadata, table_name):
        return
    where_clause = parse_condition(condition)
    check_clause(metadata, table_name, where_clause)
    table_data = load_table_data(table_name)
    ids = [row["ID"] for row in select(table_data, where_clause)]
    if not ids:
        print("Записей не найдено.")
        return
    new_data = delete(table_data, where_clause)
    if len(new_data) == len(table_data):
        return
    save_table_data(table_name, new_data)
    for record_id in ids:
        print(f'Запись с ID={record_id} успешно удалена из таблицы "{table_name}".')


def handle_info(metadata, user_input):
    words = user_input.split()
    if len(words) != 2:
        raise ValueError(user_input)
    table_name = words[1]
    if not check_table(metadata, table_name):
        return
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(metadata[table_name])}")
    print(f"Количество записей: {len(load_table_data(table_name))}")

DATA_HANDLERS = {
    "insert": handle_insert,
    "select": handle_select,
    "update": handle_update,
    "delete": handle_delete,
    "info": handle_info,
}


def run():
    print("***База данных***")
    print_help()

    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string(">>>Введите команду: ")

        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue
        if not args:
            continue

        command = args[0]
        if command in MODIFYING_COMMANDS:
            reset_cache()
        match command:
            case "create_table":
                if len(args) < 3:
                    print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                    continue
                metadata = create_table(metadata, args[1], args[2:])
                save_metadata(META_FILE, metadata)
            case "drop_table":
                if len(args) != 2:
                    print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                    continue
                metadata = drop_table(metadata, args[1])
                save_metadata(META_FILE, metadata)
            case "list_tables":
                for table_name in metadata:
                    print(f"- {table_name}")
            case "insert" | "select" | "update" | "delete" | "info":
                try:
                    DATA_HANDLERS[command](metadata, user_input)
                except ValueError as error:
                    print(f"Некорректное значение: {error}. Попробуйте снова.")
            case "help":
                print_help()
            case "exit":
                break
            case _:
                print(f"Функции {command} нет. Попробуйте снова.")