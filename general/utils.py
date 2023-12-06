from typing import List


def read_lines(file_name: str) -> List[str]:
    file = open(file_name, "r")
    lines: List[str] = []
    for line in file:
        lines.append(line.removesuffix("\n"))
    file.close()
    return lines


def read_file(file_name: str) -> str:
    file = open(file_name, "r")
    content = file.read()
    file.close()
    return content


def try_parse_int(value):
    try:
        return int(value), True
    except ValueError:
        return value, False