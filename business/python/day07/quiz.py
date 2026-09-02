from collections import defaultdict


def count_completed_orders(orders):
    completed_count = defaultdict(int)
    for order in orders:
        user = order.get("user")
        status = order.get("status")
        if status == "completed":
            completed_count[user] += 1
    return dict(completed_count)


def sales_by_city(orders):
    city_sales = defaultdict(int)
    for order in orders:
        city = order.get("city")
        amount = order.get("amount")
        status = order.get("status")
        if status == "completed":
            city_sales[city] += amount
    return dict(city_sales)


def top_users(orders, n):
    user_amount = defaultdict(int)
    for order in orders:
        user = order.get("user")
        status = order.get("status")
        amount = order.get("amount")
        if status == "completed":
            user_amount[user] += amount
    return sorted(user_amount.items(), key=lambda x: x[1], reverse=True)[:n]


def has_invalid_order(orders):
    # amount <= 0
    # status 不是 "completed" 或 "cancelled"
    # user 是 None 或空字符串
    return any(order.get("amount") <= 0
               or order.get("status") not in ["completed", "cancelled"]
               or not order.get("user")
               for order in orders)


def cities_by_user(orders):
    user_cities = defaultdict(set)
    for order in orders:
        if order.get("status") == "completed":
            user = order.get("user")
            city = order.get("city")
            user_cities[user].add(city)
    return dict(user_cities)


def completed_orders(orders):
    # 一个一个地产生 completed order，而不是一次性创建一个新的 list。
    for order in orders:
        if order.get("status") == "completed":
            yield order


def main():
    orders = [
        {"user": "Alice", "city": "Beijing", "amount": 100, "status": "completed"},
        {"user": "Bob", "city": "Shanghai", "amount": 200, "status": "completed"},
        {"user": "Alice", "city": "Beijing", "amount": 150, "status": "completed"},
        {"user": "Charlie", "city": "Beijing", "amount": 300, "status": "cancelled"},
        {"user": "Bob", "city": "Shanghai", "amount": 100, "status": "completed"},
        {"user": "Alice", "city": "Shanghai", "amount": 200, "status": "completed"},
        {"user": "David", "city": "Beijing", "amount": 250, "status": "completed"},
        {"user": "Bob", "city": "Beijing", "amount": 150, "status": "cancelled"},
        {"user": "David", "city": "Beijing", "amount": 100, "status": "completed"},
        {"user": "Alice", "city": "Beijing", "amount": 50, "status": "completed"},
    ]
    completed_count = count_completed_orders(orders)
    print(completed_count)

    city_sales = sales_by_city(orders)
    print(city_sales)

    top_user_amount = top_users(orders, 2)
    print(top_user_amount)

    has_invalid_records = has_invalid_order(orders)
    print(has_invalid_records)

    user_cities = cities_by_user(orders)
    print(user_cities)

    for order in completed_orders(orders):
        print(order)


if __name__ == '__main__':
    main()
