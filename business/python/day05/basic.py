def parse_names(text):
    return [name.strip() for name in text.strip().split(",")]


def parse_log(log):
    content_list = log.split(",")
    key_list = ["date", "level", "event", "user_id"]
    return dict(zip(key_list, content_list))


def filter_valid_records(records):
    # 只保留name 不为空，并且 age 不为 None 的记录。
    return [record for record in records
            if record.get("name") is not None
            and record.get("name") != ""
            and record.get("age") is not None]


def calculate_customer_total(orders):
    result = {}
    for order in orders:
        customer = order.get("customer")
        amount = order.get("amount", 0)
        result[customer] = result.get(customer, 0) + amount

    return result


def calculate_large_order_total(orders):
    result = {}
    for order in orders:
        amount = order.get("amount")
        if amount is not None and amount >= 100:
            customer = order.get("customer")
            result[customer] = result.get(customer, 0) + amount

    return result


def find_most_frequent(numbers):
    frequency_dict = {}
    for number in numbers:
        frequency_dict[number] = frequency_dict.get(number, 0) + 1

    most_frequent = None
    max_count = 0
    for number, count in frequency_dict.items():
        if count > max_count:
            max_count = count
            most_frequent = number
    return most_frequent


def calculate_average_age_by_city(users):
    city_total = {}
    city_count = {}
    result = {}
    for user in users:
        city = user.get("city")
        age = user.get("age", 0)
        city_total[city] = city_total.get(city, 0) + age
        city_count[city] = city_count.get(city, 0) + 1
    for city, total in city_total.items():
        result[city] = round(total / city_count[city], 2)

    return result


def calculate_completed_total(transactions):
    result = {}
    for transaction in transactions:
        status = transaction.get("status")
        user = transaction.get("user")
        amount = transaction.get("amount")
        if status is not None and status.lower() == "completed":
            result[user] = result.get(user, 0) + amount
    return result


def main():
    text = "  Alice, Bob, Charlie, David  "
    # 字符串清洗
    name_list = parse_names(text)
    print(name_list)
    print("---------------------------")

    # 字段解析
    log = "2026-08-31,INFO,user_login,12345"
    log_dict = parse_log(log)
    print(log_dict)
    print("---------------------------")

    # 过滤无效数据
    records = [
        {"id": 1, "name": "Alice", "age": 25},
        {"id": 2, "name": "", "age": 30},
        {"id": 3, "name": "Charlie", "age": None},
        {"id": 4, "name": "David", "age": 28},
        {"id": 5, "name": None, "age": 22}
    ]

    valid_records = filter_valid_records(records)
    print(valid_records)
    print("---------------------------")

    # 统计每个 customer 的订单总金额。
    orders = [
        {"customer": "Alice", "amount": 100},
        {"customer": "Bob", "amount": 200},
        {"customer": "Alice", "amount": 150},
        {"customer": "Charlie", "amount": 80},
        {"customer": "Bob", "amount": 120}
    ]
    customer_total = calculate_customer_total(orders)
    print(customer_total)
    print("---------------------------")

    # 只统计 amount >= 100 的订单，然后计算每个 customer 的总金额。
    orders = [
        {"customer": "Alice", "amount": 100},
        {"customer": "Bob", "amount": 200},
        {"customer": "Alice", "amount": 150},
        {"customer": "Charlie", "amount": 80},
        {"customer": "Bob", "amount": 120}
    ]
    customer_total = calculate_large_order_total(orders)
    print(customer_total)
    print("---------------------------")

    # 找出出现频率最高的元素
    numbers = [4, 7, 2, 7, 4, 9, 2, 7, 5]
    result = find_most_frequent(numbers)
    print(result)
    print("---------------------------")

    # 要求计算每个城市的平均年龄。
    users = [
        {"name": "Alice", "age": 25, "city": "Beijing"},
        {"name": "Bob", "age": 30, "city": "Shanghai"},
        {"name": "Charlie", "age": 35, "city": "Beijing"},
        {"name": "David", "age": 28, "city": "Shanghai"},
        {"name": "Eva", "age": 22, "city": "Beijing"}
    ]
    result = calculate_average_age_by_city(users)
    print(result)
    print("---------------------------")

    # 只统计 status == "completed" 的交易，并计算每个 user 的 total amount。
    transactions = [
        {"user": "Alice", "amount": 100, "status": "completed"},
        {"user": "Bob", "amount": 200, "status": "cancelled"},
        {"user": "Alice", "amount": 150, "status": "completed"},
        {"user": "Bob", "amount": 120, "status": "completed"},
        {"user": "Charlie", "amount": 80, "status": "completed"},
        {"user": "Alice", "amount": 50, "status": "cancelled"}
    ]
    result = calculate_completed_total(transactions)
    print(result)


if __name__ == "__main__":
    main()
