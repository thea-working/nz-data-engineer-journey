def calculate_average(numbers):
    return sum(numbers) / len(numbers)


def get_even_numbers(numbers):
    return [num for num in numbers if num % 2 == 0]


def calculate_sum(start, end):
    total = 0
    for num in range(start, end + 1):
        total += num

    return total


def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


def clean_text(text):
    return text.strip().lower()


def count_word(text, word):
    count = 0
    for w in text.split():
        if w.lower() == word.lower():
            count += 1

    return count


def calculate_total(*args):
    return sum(args)


def build_config(**kwargs):
    return kwargs


def main():
    numbers = [10, 20, 30, 40, 50]
    result = calculate_average(numbers)
    print(result)
    print("--------------------------")

    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    result = get_even_numbers(numbers)
    print(result)
    print("--------------------------")

    result = calculate_sum(1, 5)
    print(result)
    print("--------------------------")

    result = greet("Alice")
    print(result)
    result = greet("Alice", "Good morning")
    print(result)
    print("--------------------------")

    text = "  Data Engineer Python  "
    result = clean_text(text)
    print(result)
    print("--------------------------")

    text = "python is easy and Python is powerful"
    result = count_word(text, "python")
    print(result)
    print("--------------------------")

    result = calculate_total(5, 10, 15, 20, 25)
    print(result)
    result = calculate_total()
    print(result)
    print("--------------------------")

    config = build_config(
        host="localhost",
        port=5432,
        database="sales"
    )
    print(config)


if __name__ == '__main__':
    main()
