def parse_value(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False
    if text.isdigit():
        return int(text)
    raise ValueError(text)


def parse_condition(text):
    column, sep, value = text.partition("=")
    if not sep or not column.strip():
        raise ValueError(text)
    return {column.strip(): parse_value(value)}


def parse_values(text):
    text = text.strip()
    if not (text.startswith("(") and text.endswith(")")):
        raise ValueError(text)
    return [parse_value(part) for part in text[1:-1].split(",")]