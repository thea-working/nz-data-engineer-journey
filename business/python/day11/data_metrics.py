from black.trans import defaultdict


def filter_valid_transactions(transactions):
    valid_transactions = []
    for transaction in transactions:
        if (transaction["status"] == "completed"
                and transaction["user"]
                and transaction["category"]
                and transaction["amount"] > 0
        ):
            valid_transactions.append(transaction)
    return valid_transactions


def calculate_user_sales(transactions):
    valid_transactions = filter_valid_transactions(transactions)
    user_sales = defaultdict(int)
    for transaction in valid_transactions:
        user_sales[transaction["user"]] += transaction["amount"]
    return dict(user_sales)


def get_top_users(transactions, n):
    user_sales = calculate_user_sales(transactions)
    return sorted(user_sales.items(), key=lambda x: x[1], reverse=True)[:n]


def calculate_category_sales(transactions):
    valid_transactions = filter_valid_transactions(transactions)
    category_sales = defaultdict(int)
    for transaction in valid_transactions:
        category_sales[transaction["category"]] += transaction["amount"]
    return dict(category_sales)


def generate_metrics_report(transactions, n):
    top_users = get_top_users(transactions, n)
    category_sales = calculate_category_sales(transactions)
    return {
        "top_users": top_users,
        "category_sales": category_sales
    }


def main():
    transactions = [
        {"user": "Alice", "category": "Electronics", "amount": 120, "status": "completed"},
        {"user": "Bob", "category": "Books", "amount": 50, "status": "completed"},
        {"user": "Alice", "category": "Books", "amount": 30, "status": "cancelled"},
        {"user": "Charlie", "category": "Electronics", "amount": 200, "status": "completed"},
        {"user": "Bob", "category": "Electronics", "amount": -10, "status": "completed"},
        {"user": "", "category": "Books", "amount": 80, "status": "completed"},
        {"user": "David", "category": "", "amount": 100, "status": "completed"},
    ]

    valid_transactions = filter_valid_transactions(transactions)
    print(valid_transactions)
    print("----------------------------------------")

    user_sales = calculate_user_sales(transactions)
    print(user_sales)
    print("----------------------------------------")

    top_users = get_top_users(transactions, 2)
    print(top_users)
    print("----------------------------------------")

    category_sales = calculate_category_sales(transactions)
    print(category_sales)
    print("----------------------------------------")

    metrics = generate_metrics_report(transactions, 2)
    print(metrics)


if __name__ == "__main__":
    main()
