import json
from collections import defaultdict


def clean_orders(orders):
    # user 去掉首尾空格
    # user 为空的记录丢弃
    # amount 转换成 float
    # amount 无法转换的记录丢弃
    # 只保留 status == "completed" 的订单
    # amount <= 0 的订单丢弃
    # 返回清洗后的订单列表
    result = []
    for order in orders:
        user = order["user"].strip()
        try:
            amount = float(order["amount"])
        except (TypeError, ValueError):
            continue

        if not user or amount <= 0 or order["status"] != "completed":
            continue

        # copy浅拷贝，便于扩展其他字段；若order包含嵌套list,dict则用copy.deepcopy()
        cleaned_order = order.copy()
        cleaned_order["user"] = user
        cleaned_order["amount"] = amount

        result.append(cleaned_order)
    return result


def calculate_user_sales(orders):
    cleaned_orders = clean_orders(orders)
    user_sales = defaultdict(int)
    for order in cleaned_orders:
        user_sales[order["user"]] += order["amount"]
    return dict(user_sales)


def get_top_users(orders, n):
    user_sales = calculate_user_sales(orders)
    sorted_user_sales = sorted(user_sales.items(), key=lambda x: x[1], reverse=True)[:n]
    return sorted_user_sales


def parse_orders_json(orders_json):
    json_orders = json.loads(orders_json)
    return json_orders


def process_orders(orders_json, n):
    # JSON 字符串 → 解析 → 清洗 → 计算用户销售额 → 获取 Top N
    json_orders = parse_orders_json(orders_json)
    user_sales = calculate_user_sales(json_orders)
    total_sales = sum(user_sales.values())
    top_users = get_top_users(json_orders, n)
    return {
        "top_users": top_users,
        "total_sales": total_sales
    }


def main():
    orders = [
        {"order_id": "1001", "user": " Alice ", "amount": "120.5", "status": "completed"},
        {"order_id": "1002", "user": "Bob", "amount": "80", "status": "completed"},
        {"order_id": "1003", "user": "", "amount": "50", "status": "completed"},
        {"order_id": "1004", "user": " Charlie ", "amount": "invalid", "status": "completed"},
        {"order_id": "1005", "user": "David", "amount": "100", "status": "cancelled"},
        {"order_id": "1006", "user": " Alice ", "amount": "200", "status": "completed"},
    ]
    result = clean_orders(orders)
    print(result)
    print("------------------------------------")

    user_sales = calculate_user_sales(result)
    print(user_sales)
    print("------------------------------------")

    top_users = get_top_users(orders, 2)
    print(top_users)
    print("-------------------------------------")

    orders_json = """
    [
        {"order_id": "1001", "user": " Alice ", "amount": "120.5", "status": "completed"},
        {"order_id": "1002", "user": "Bob", "amount": "80", "status": "completed"},
        {"order_id": "1003", "user": "", "amount": "50", "status": "completed"},
        {"order_id": "1004", "user": " Charlie ", "amount": "invalid", "status": "completed"},
        {"order_id": "1005", "user": "David", "amount": "100", "status": "cancelled"},
        {"order_id": "1006", "user": " Alice ", "amount": "200", "status": "completed"}
    ]
    """

    json_orders = json.loads(orders_json)
    print(json_orders)
    print("------------------------------------")

    result = process_orders(orders_json, n=2)
    print(result)


if __name__ == "__main__":
    main()
