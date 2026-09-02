from collections import Counter
from collections import defaultdict


def count_frequency(numbers):
    return dict(Counter(numbers))


def top_frequent(numbers, n):
    return dict(Counter(numbers).most_common(n))


def aggregate_orders(orders):
    result = defaultdict(int)
    for name, amount in orders:
        result[name] += amount
    return result


def group_users_by_city(users):
    result = defaultdict(list)
    for name, city in users:
        result[city].append(name)
    return dict(result)


def group_unique_cities(visits):
    result = defaultdict(set)
    for name, city in visits:
        result[name].add(city)
    return dict(result)


def validate_ages(ages):
    # return all(age >= 18 for age in ages)
    return any(age >= 18 for age in ages)


def even_numbers(numbers):
    for num in numbers:
        if num % 2 == 0:
            yield num


def get_top_users(orders, n):
    user_amount = defaultdict(int)
    for order in orders:
        user = order.get("user")
        amount = order.get("amount")
        status = order.get("status")
        if status is not None and status.lower() == 'completed':
            user_amount[user] += amount
    return sorted(user_amount.items(), key=lambda x: x[1], reverse=True)[:n]


def main():
    numbers = [1, 2, 2, 3, 1, 4, 2, 3, 5, 1]
    result = count_frequency(numbers)
    print(result)
    print("---------------------------")

    numbers = [1, 2, 2, 3, 1, 4, 2, 3, 5, 1, 3, 3]
    result = top_frequent(numbers, 2)
    print(result)
    print("---------------------------")

    orders = [
        ("Alice", 100),
        ("Bob", 200),
        ("Alice", 150),
        ("Charlie", 300),
        ("Bob", 100),
    ]
    result = aggregate_orders(orders)
    print(result)
    print("---------------------------")

    users = [
        ("Alice", "Beijing"),
        ("Bob", "Shanghai"),
        ("Charlie", "Beijing"),
        ("David", "Shanghai"),
        ("Eve", "Beijing"),
    ]
    result = group_users_by_city(users)
    print(result)
    print("---------------------------")

    visits = [
        ("Alice", "Beijing"),
        ("Alice", "Shanghai"),
        ("Alice", "Beijing"),
        ("Bob", "Shanghai"),
        ("Bob", "Beijing"),
        ("Bob", "Shanghai"),
    ]
    result = group_unique_cities(visits)
    print(result)
    print("---------------------------")

    ages = [25, 31, 18, 42, 16]
    result = validate_ages(ages)
    print(result)
    print("---------------------------")

    numbers = [1, 2, 3, 4, 5]
    result = even_numbers(numbers)
    for num in result:
        print(num)
    print("---------------------------")

    orders = [
        {"user": "Alice", "amount": 100, "status": "completed"},
        {"user": "Bob", "amount": 200, "status": "completed"},
        {"user": "Alice", "amount": 150, "status": "cancelled"},
        {"user": "Charlie", "amount": 300, "status": "completed"},
        {"user": "Bob", "amount": 100, "status": "completed"},
        {"user": "Alice", "amount": 200, "status": "completed"},
    ]
    result = get_top_users(orders, 2)
    print(result)


if __name__ == "__main__":
    main()
