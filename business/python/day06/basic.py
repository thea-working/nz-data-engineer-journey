def get_top_users(users, threshold):
    # 返回 score >= threshold 的用户姓名列表。
    return [user.get("name") for user in users
            if user.get("score", 0) >= threshold
            ]


def calculate_order_total(order):
    total = 0
    for item in order.get("items", []):
        item_quantity = item.get("quantity", 0)
        item_price = item.get("price", 0)
        total += item_quantity * item_price
    return total


def calculate_customer_spending(orders):
    result = {}
    for order in orders:
        customer = order.get("customer")
        order_total = calculate_order_total(order)
        result[customer] = result.get(customer, 0) + order_total
    return result


def find_top_customer(orders):
    customer_spending = calculate_customer_spending(orders)
    max_spent = float("-inf")
    max_spent_customer = ""
    for customer in customer_spending:
        if customer_spending[customer] > max_spent:
            max_spent = customer_spending[customer]
            max_spent_customer = customer
    return max_spent_customer
    # max_spending = max(customer_spending, key=customer_spending.get)
    # return max_spending


def deduplicate_users(users):
    seen = set()
    distinct_users = []
    for user in users:
        user_id = user.get("id")
        if user_id not in seen:
            distinct_users.append(user)
            seen.add(user_id)
    return distinct_users


def deduplicate_records(records):
    # 根据 (user_id, product_id) 联合去重，保留第一次出现的记录。
    seen = set()
    distinct_records = []
    for record in records:
        key = (record.get("user_id"), record.get("product_id"))
        if key not in seen:
            distinct_records.append(record)
            seen.add(key)
    return distinct_records


def find_duplicates(ids):
    # 找出所有出现超过一次的 ID，每个 ID 在结果中只出现一次。
    seen = set()
    duplicates = set()
    for num in ids:
        if num not in seen:
            seen.add(num)
        else:
            duplicates.add(num)
    return list(duplicates)


def get_top_spending_users(transactions, threshold):
    # {"user_id": 1, "amount": 100, "status": "completed"},
    user_total = {}
    for user in transactions:
        if user.get("status") is not None and user.get("status") == "completed":
            user_id = user.get("user_id")
            amount = user.get("amount")
            user_total[user_id] = user_total.get(user_id, 0) + amount

    return [
        user_id
        for user_id, user_total in user_total.items()
        if user_total >= threshold
    ]


def main():
    users = [
        {"id": 1, "name": "Alice", "score": 85},
        {"id": 2, "name": "Bob", "score": 92},
        {"id": 3, "name": "Charlie", "score": 78},
        {"id": 4, "name": "David", "score": 95},
        {"id": 5, "name": "Eva", "score": 88}
    ]

    result = get_top_users(users, 90)
    print(result)
    print("---------------------------------")

    orders = [
        {
            "order_id": 101,
            "customer": "Alice",
            "items": [
                {"product": "Laptop", "quantity": 1, "price": 1000},
                {"product": "Mouse", "quantity": 2, "price": 25}
            ]
        },
        {
            "order_id": 102,
            "customer": "Bob",
            "items": [
                {"product": "Keyboard", "quantity": 1, "price": 80},
                {"product": "Mouse", "quantity": 1, "price": 25}
            ]
        }
    ]

    result = calculate_order_total(orders[0])
    print(result)
    print("-------------------------------")

    result = calculate_customer_spending(orders)
    print(result)
    print("--------------------------------")

    result = find_top_customer(orders)
    print(result)
    print("-------------------------------")

    users = [
        {"id": 1, "name": "Alice", "city": "Beijing"},
        {"id": 2, "name": "Bob", "city": "Shanghai"},
        {"id": 1, "name": "Alice", "city": "Beijing"},
        {"id": 3, "name": "Charlie", "city": "Beijing"},
        {"id": 2, "name": "Bob", "city": "Shanghai"}
    ]

    distinct_users = deduplicate_users(users)
    print(distinct_users)
    print("------------------------------")

    records = [
        {"user_id": 1, "product_id": 101, "amount": 100},
        {"user_id": 1, "product_id": 102, "amount": 200},
        {"user_id": 1, "product_id": 101, "amount": 100},
        {"user_id": 2, "product_id": 101, "amount": 150},
        {"user_id": 1, "product_id": 102, "amount": 200}
    ]

    distinct_records = deduplicate_records(records)
    print(distinct_records)
    print("------------------------------")

    ids = [101, 102, 103, 101, 104, 102, 105, 101]
    result = find_duplicates(ids)
    print(result)
    print("------------------------------")

    transactions = [
        {"user_id": 1, "amount": 100, "status": "completed"},
        {"user_id": 2, "amount": 200, "status": "cancelled"},
        {"user_id": 1, "amount": 150, "status": "completed"},
        {"user_id": 3, "amount": 80, "status": "completed"},
        {"user_id": 2, "amount": 120, "status": "completed"},
        {"user_id": 1, "amount": 50, "status": "cancelled"},
        {"user_id": 3, "amount": 120, "status": "completed"}
    ]

    result = get_top_spending_users(transactions, 200)
    print(result)


if __name__ == "__main__":
    main()
