def clean_users(users):
    cleaned_users = []
    for user in users:
        user_name = user["name"]
        user_email = user["email"]
        user_age = user["age"]
        if user_name and user_email and user_age is not None:
            user_name = user_name.strip()
            user_email = user_email.lower()
            cleaned_users.append({
                "name": user_name,
                "email": user_email,
                "age": user_age
            })
    return cleaned_users


def normalize_emails(users):
    normalized_users = []
    for user in users:
        normalized_users.append({
            "name": user["name"],
            "email": user["email"].strip().lower()
        })
    return normalized_users


def deduplicate_users(users):
    deduplicated_users = []
    seen = set()
    for user in users:
        if user["email"] not in seen:
            deduplicated_users.append(user)
            seen.add(user["email"])
    return deduplicated_users


def deduplicate_orders(orders):
    deduplicated_orders = []
    seen = set()
    for order in orders:
        if (order["user"], order["product"]) not in seen:
            deduplicated_orders.append(order)
            seen.add((order["user"], order["product"]))
    return deduplicated_orders


def process_orders(orders):
    processed_orders = []
    seen = set()
    for order in orders:
        user = order["user"].strip()
        product = order["product"].strip()
        amount = order["amount"]
        status = order["status"]

        try:
            amount = int(amount)
        except (TypeError, ValueError):
            continue

        if (
                user
                and product
                and amount > 0
                and status == "completed"
                and (user, product) not in seen
        ):
            processed_orders.append({
                "user": user,
                "product": product,
                "amount": amount,
                "status": status
            })
            seen.add((user, product))
    return processed_orders


def main():
    users = [
        {"name": " Alice ", "email": "ALICE@example.com", "age": 25},
        {"name": "Bob", "email": "bob@example.com", "age": 30},
        {"name": "", "email": "charlie@example.com", "age": 28},
        {"name": " David ", "email": "", "age": 35},
        {"name": "Eve", "email": "eve@example.com", "age": None},
    ]
    cleaned_users = clean_users(users)
    print(cleaned_users)
    print("---------------------------------")

    users = [
        {"name": "Alice", "email": " Alice@Example.COM "},
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Charlie", "email": " CHARLIE@EXAMPLE.COM"},
        {"name": "David", "email": "david@example.com "},
    ]

    normalized_users = normalize_emails(users)
    print(normalized_users)
    print("--------------------------------")

    users = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
        {"name": "Alice Smith", "email": "alice@example.com"},
        {"name": "Charlie", "email": "charlie@example.com"},
        {"name": "Bob Lee", "email": "bob@example.com"},
    ]
    deduplicated_users = deduplicate_users(users)
    print(deduplicated_users)
    print("------------------------------")

    orders = [
        {"user": "Alice", "product": "Laptop", "amount": 1000},
        {"user": "Bob", "product": "Phone", "amount": 500},
        {"user": "Alice", "product": "Laptop", "amount": 1000},
        {"user": "Alice", "product": "Phone", "amount": 500},
        {"user": "Bob", "product": "Phone", "amount": 500},
    ]
    deduplicated_orders = deduplicate_orders(orders)
    print(deduplicated_orders)
    print("------------------------------")

    orders = [
        {"user": " Alice ", "product": "Laptop", "amount": "1000", "status": "completed"},
        {"user": "Bob", "product": "Phone", "amount": "500", "status": "completed"},
        {"user": "Alice", "product": "Laptop", "amount": "1000", "status": "completed"},
        {"user": "", "product": "Tablet", "amount": "300", "status": "completed"},
        {"user": "Charlie", "product": "Phone", "amount": "invalid", "status": "completed"},
        {"user": "David", "product": "Laptop", "amount": "-100", "status": "completed"},
        {"user": "Bob", "product": "Phone", "amount": "500", "status": "cancelled"},
    ]
    processed_orders = process_orders(orders)
    print(processed_orders)


if __name__ == "__main__":
    main()
