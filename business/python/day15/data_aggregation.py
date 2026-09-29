from collections import defaultdict


def count_user_actions(events):
    user_actions = defaultdict(lambda: defaultdict(int))
    for event in events:
        user = event["user"]
        action = event["action"]
        user_actions[user][action] += 1

    return {
        user: dict(actions)
        for user, actions in user_actions.items()
    }


def calculate_user_category_sales(orders):
    user_category_sales = defaultdict(lambda: defaultdict(int))
    for order in orders:
        user = order["user"]
        category = order["category"]
        amount = order["amount"]
        user_category_sales[user][category] += amount

    return {
        user: dict(category_sales)
        for user, category_sales in user_category_sales.items()
    }


def get_top_category_by_user(orders):
    user_category_sales = calculate_user_category_sales(orders)
    result = {}
    # for user, category_sales in user_category_sales.items():
    #     top_category_amount = sorted(category_sales.items(), key=lambda x: x[1], reverse=True)[:1]
    #     result[user] = top_category_amount[0]
    for user, category_sales in user_category_sales.items():
        top_category = max(
            category_sales.items(),
            key=lambda x: x[1]
        )
        result[user] = top_category

    return result


def calculate_category_metrics(orders):
    category_metrics = defaultdict(lambda: defaultdict(int))
    for order in orders:
        category = order["category"]
        amount = order["amount"]
        category_metrics[category]["order_count"] += 1
        category_metrics[category]["total_sales"] += amount

    return {
        category: dict(category_metric)
        for category, category_metric in category_metrics.items()
    }


def generate_sales_report(orders):
    category_metrics = calculate_category_metrics(orders)
    top_category_by_user = get_top_category_by_user(orders)
    return {
        "category_metrics": category_metrics,
        "top_category_by_user": top_category_by_user
    }


def main():
    events = [
        {"user": "Alice", "action": "view"},
        {"user": "Bob", "action": "purchase"},
        {"user": "Alice", "action": "view"},
        {"user": "Charlie", "action": "view"},
        {"user": "Bob", "action": "view"},
        {"user": "Alice", "action": "purchase"},
        {"user": "Bob", "action": "purchase"},
        {"user": "Alice", "action": "view"},
    ]
    user_actions = count_user_actions(events)
    print(user_actions)
    print("-----------------------------------------")

    orders = [
        {"user": "Alice", "category": "Electronics", "amount": 120},
        {"user": "Bob", "category": "Books", "amount": 50},
        {"user": "Alice", "category": "Books", "amount": 30},
        {"user": "Bob", "category": "Electronics", "amount": 80},
        {"user": "Alice", "category": "Electronics", "amount": 200},
    ]
    category_sales = calculate_user_category_sales(orders)
    print(category_sales)
    print("-------------------------------------------")

    top_category_user = get_top_category_by_user(orders)
    print(top_category_user)
    print("-------------------------------------------")

    orders = [
        {"user": "Alice", "category": "Electronics", "amount": 120},
        {"user": "Bob", "category": "Books", "amount": 50},
        {"user": "Alice", "category": "Books", "amount": 30},
        {"user": "Bob", "category": "Electronics", "amount": 80},
        {"user": "Alice", "category": "Electronics", "amount": 200},
    ]
    category_metrics = calculate_category_metrics(orders)
    print(category_metrics)
    print("--------------------------------------------")

    orders = [
        {"user": "Alice", "category": "Electronics", "amount": 120},
        {"user": "Bob", "category": "Books", "amount": 50},
        {"user": "Alice", "category": "Books", "amount": 30},
        {"user": "Bob", "category": "Electronics", "amount": 80},
        {"user": "Alice", "category": "Electronics", "amount": 200},
        {"user": "Charlie", "category": "Books", "amount": 100},
    ]
    sales_report = generate_sales_report(orders)
    print(sales_report)


if __name__ == "__main__":
    main()
