from typing import List, Dict

string_to_digit_lookup_dict: Dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def try_parse_int(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def try_parse_digit(index, text):
    try:
        return int(text[index]), True
    except ValueError:
        substring = text[index:]
        for digit_string in string_to_digit_lookup_dict.keys():
            if substring.startswith(digit_string):
                digit = string_to_digit_lookup_dict.get(digit_string)
                return digit, True
        return text, False


def read_lines(file_name: str):
    file = open(file_name, "r")
    lines: List[str] = []
    for line in file:
        lines.append(line)
    file.close()
    return lines


def get_first_digit(text: str) -> int:
    for char in text:
        res, success = try_parse_int(char)
        if success:
            return res


def get_first_digit_2(text: str) -> int:
    for index in range(len(text)):
        res, success = try_parse_digit(index, text)
        if success:
            return res


def get_last_digit_2(text:str) -> int:
    for index in range(len(text)-1, -1, -1):
        res, success = try_parse_digit(index, text)
        if success:
            return res


def reverse(text: str) -> str:
    return text[::-1]


def get_last_digit(text: str):
    text_reversed = reverse(text)
    return get_first_digit(text_reversed)


def solve_first_problem(file_name: str) -> int:
    lines = read_lines(file_name)
    numbers: List[int] = []
    for line in lines:
        first_digit = get_first_digit(line)
        last_digit = get_last_digit(line)
        combined_number = 10*first_digit + last_digit
        numbers.append(combined_number)
    return sum(numbers)


def solve_second_problem(file_name: str) -> int:
    lines = read_lines(file_name)
    numbers: List[int] = []
    for line in lines:
        first_digit = get_first_digit_2(line)
        last_digit = get_last_digit_2(line)
        combined_number = 10*first_digit + last_digit
        numbers.append(combined_number)
    return sum(numbers)


if __name__ == '__main__':
    input_file_name = "input.txt"
    # input_file_name = "smaller_input.txt"
    result = solve_first_problem(input_file_name)
    print(result)
    result2 = solve_second_problem(input_file_name)
    print(result2)
