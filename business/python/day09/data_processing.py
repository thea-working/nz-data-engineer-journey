def clean_orders(orders):
    # 要求：只保留 status == "completed" 的订单
    # user 不能为空
    # amount 必须能够转换成整数
    # amount 必须大于 0
    # 返回清洗后的订单
    result = []
    for order in orders:
        user = order["user"]
        amount = order["amount"]
        status = order["status"]
        if status != "completed" or not user:
            continue
        try:
            amount = int(amount)
        except ValueError:
            continue

        if amount <= 0:
            continue

        cleaned_order = order.copy()
        cleaned_order["amount"] = amount

        result.append(cleaned_order)
    return result


def calculate_user_sales(orders):
    # 计算每个用户的总消费金额
    cleaned_orders = clean_orders(orders)
    user_sales = {}
    for order in cleaned_orders:
        user = order["user"]
        amount = order["amount"]
        user_sales[user] = user_sales.get(user, 0) + amount
    return user_sales


def get_top_users(orders, n):
    # 接收原始 orders
    # 调用 calculate_user_sales(orders)
    # 按消费金额从高到低排序
    # 返回前 n 个用户
    # 返回格式为 list of tuples
    user_sales = calculate_user_sales(orders)
    sorted_user_sales = sorted(user_sales.items(), key=lambda x: x[1], reverse=True)[:n]
    return sorted_user_sales


def calculate_city_sales(orders):
    # 只统计 completed 订单
    # 忽略无效订单
    # 按 city 聚合销售额
    # 返回 dict
    cleaned_orders = clean_orders(orders)
    city_sales = {}
    for order in cleaned_orders:
        city = order["city"]
        amount = order["amount"]
        city_sales[city] = city_sales.get(city, 0) + amount
    return city_sales


def generate_sales_report(orders, n):
    # 清洗订单
    # 计算每个用户的销售额
    # 找出消费最高的 Top N 用户
    # 计算每个城市的销售额
    # 返回一个字典：
    top_users = get_top_users(orders, n)
    city_sales = calculate_city_sales(orders)
    return {
        "top_users": top_users,
        "city_sales": city_sales
    }


def main():
    orders = [
        {"user": "Alice", "amount": "100", "status": "completed"},
        {"user": "Bob", "amount": "200", "status": "completed"},
        {"user": "Alice", "amount": "invalid", "status": "completed"},
        {"user": "Charlie", "amount": "-50", "status": "completed"},
        {"user": "", "amount": "300", "status": "completed"},
        {"user": "David", "amount": "400", "status": "cancelled"},
        {"user": "Alice", "amount": "150", "status": "completed"},
    ]

    cleaned_orders = clean_orders(orders)
    print(cleaned_orders)
    print("---------------------------------")

    user_sales = calculate_user_sales(orders)
    print(user_sales)
    print("---------------------------------")

    top_users = get_top_users(cleaned_orders, 2)
    print(top_users)
    print("--------------------------------")

    orders = [
        {"user": "Alice", "city": "Beijing", "amount": "100", "status": "completed"},
        {"user": "Bob", "city": "Shanghai", "amount": "200", "status": "completed"},
        {"user": "Alice", "city": "Beijing", "amount": "invalid", "status": "completed"},
        {"user": "Charlie", "city": "Beijing", "amount": "-50", "status": "completed"},
        {"user": "", "city": "Shanghai", "amount": "300", "status": "completed"},
        {"user": "David", "city": "Beijing", "amount": "400", "status": "cancelled"},
        {"user": "Alice", "city": "Shanghai", "amount": "150", "status": "completed"},
    ]
    city_sales = calculate_city_sales(orders)
    print(city_sales)
    print("-------------------------------")

    sales_report = generate_sales_report(orders, 2)
    print(sales_report)


if __name__ == '__main__':
    main()
