import uuid


def generate_uuid():
    return uuid.uuid4()


def flatten(arr):
    result = []
    for item in arr:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def str_to_float(text: str) -> float:
    try:
        value = float(text.replace(',', ''))
        return value
    except Exception:
        return 0.0
