VALID_TYPES = ("int", "str", "bool")


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = ["ID:int"]
    for column in columns:
        name, _, column_type = column.partition(":")
        if not name or column_type not in VALID_TYPES:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        table_columns.append(column)

    metadata[table_name] = table_columns
    columns_text = ", ".join(table_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_text}')
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata