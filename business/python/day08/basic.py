import json
import csv
from collections import defaultdict


def calculate_average_age(ages):
    sum_age = 0
    valid_num = 0

    for age in ages:
        try:
            if age > 0:
                sum_age += age
                valid_num += 1
        except TypeError:
            continue

    return sum_age / valid_num if valid_num else 0


def process_order(order):
    # order_id 不存在或者为空 → 抛出 ValueError
    # amount 小于 0 → 抛出 ValueError
    # status 不是 "completed" 或 "cancelled" → 抛出 ValueError
    order_id = order.get("order_id")
    amount = order.get("amount")
    status = order.get("status")
    if not order_id or amount < 0 or status not in ["completed", "cancelled"]:
        raise ValueError("Invalid order data")

    return f"Order {order_id} is valid"


def read_users(filename):
    result = []
    with open(filename) as f:
        for line in f:
            name, age, city = line.strip().split(",")
            result.append(
                {
                    "name": name,
                    "age": int(age),
                    "city": city
                }
            )
    return result


def load_orders(filename):
    with open(filename) as f:
        json_data = json.load(f)

    return json_data


def load_completed_orders(filename):
    result = []
    with open(filename) as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row.get("status") == "completed":
                result.append(
                    {
                        "order_id": row.get("order_id"),
                        "user": row.get("user"),
                        "amount": int(row.get("amount"))
                    }
                )
    return result


def load_valid_orders(filename):
    # 读取并清洗有效订单
    # order_id 不能为空
    # user 不能为空
    # amount 必须能够转换成数字
    # amount > 0
    # status 必须是 "completed" 或 "cancelled"
    result = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_id = row.get("order_id")
            user = row.get("user")
            amount = row.get("amount")
            status = row.get("status")
            if not order_id or not user or status not in [
                "completed", "cancelled"]:
                continue
            try:
                amount = int(amount)
            except ValueError:
                continue

            if amount <= 0:
                continue
            result.append(
                {
                    "order_id": order_id,
                    "user": user,
                    "amount": amount,
                    "status": status
                }
            )

    return result


def calculate_user_sales(orders):
    # 只统计 completed 订单
    # 按 user 聚合 amount
    # 返回一个普通 dict
    result = defaultdict(int)
    for order in orders:
        if order.get("status") == "completed":
            result[order.get("user")] += order.get("amount")
    return dict(result)


def get_top_users(sales, n):
    sorted_sales = sorted(sales.items(), key=lambda x: x[1], reverse=True)[:n]
    return sorted_sales


def main():
    ages = [25, 30, "unknown", 28, None, 35]
    avg_age = calculate_average_age(ages)
    print(avg_age)
    print("--------------------------------")

    order = {
        "order_id": "A001",
        "amount": 100,
        "status": "completed"
    }
    valid_check = process_order(order)
    print(valid_check)
    print("------------------------------")

    filename = "users.txt"
    result = read_users(filename)
    print(result)
    print("------------------------------")

    filename = "orders.json"
    json_data = load_orders(filename)
    total = sum(order.get("amount", 0) for order in json_data)

    print(total)
    print("------------------------------")

    filename = "orders.csv"
    completed_orders = load_completed_orders(filename)
    print(completed_orders)
    print("------------------------------")

    orders_dirty_filename = "orders_dirty.csv"
    cleaned_orders = load_valid_orders(orders_dirty_filename)
    print(cleaned_orders)
    print("-------------------------------")

    user_sales = calculate_user_sales(cleaned_orders)
    print(user_sales)
    print("-------------------------------")

    top_users = get_top_users(user_sales, 2)
    print(top_users)


if __name__ == "__main__":
    main()
