def main():
    # Q1: 请生成一个新的列表，其中每个元素都是原数字的平方。
    numbers = [1, 2, 3, 4, 5]
    num_squares = []
    for num in numbers:
        num_squares.append(num ** 2)
    # num_squares = [num ** 2 for num in numbers]
    print(num_squares)
    print('---------------------')

    # Q2: 筛选偶数并计算平方
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    # num_squares = []
    # for num in numbers:
    #     if num % 2 == 0:
    #         num_squares.append(num ** 2)
    num_squares = [num ** 2 for num in numbers if num % 2 == 0]
    print(num_squares)
    print('---------------------')

    # Q3: 使用 list comprehension，生成一个新列表：只包含大于 5 的数字。
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num_list = [num for num in numbers if num > 5]
    print(num_list)
    print('---------------------')

    # Q4: 找出所有偶数，并将它们转换成字符串。
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    char_list = [str(num) for num in numbers if num % 2 == 0]
    print(char_list)
    print('---------------------')

    # Q5: 使用 List Comprehension，生成一个新列表：将每个名字转换成大写。
    names = ["alice", "bob", "charlie", "david"]
    upper_list = [name.upper() for name in names]
    print(upper_list)
    print('---------------------')

    # Q6 : 根据两个列表创建字典
    keys = ["name", "age", "city"]
    values = ["Alice", 30, "Beijing"]
    students = {}
    for i in range(len(keys)):
        students[keys[i]] = values[i]
    print(students)
    print('---------------------')

    # Q7: dict遍历, 请找出分数大于等于 90 的学生姓名。
    scores = {
        "Alice": 85,
        "Bob": 92,
        "Charlie": 78,
        "David": 95
    }
    # stu_list = [name for name in scores.keys() if scores[name] >= 90]
    stu_list = [name for name, score in scores.items() if score >= 90]
    print(stu_list)
    print('---------------------')

    # Q8: 请找出所有成年用户（age >= 18），生成一个新的 list。
    users = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 17},
        {"name": "Charlie", "age": 30},
        {"name": "David", "age": 16},
        {"name": "Eva", "age": 22}
    ]
    adult_users = [user for user in users if user.get("age", 0) >= 18]
    print(adult_users)
    print('---------------------')

    # Q9:请找出所有：订单金额大于等于 100 的订单 ID
    orders = [
        {"order_id": 101, "amount": 120},
        {"order_id": 102, "amount": 80},
        {"order_id": 103, "amount": 250},
        {"order_id": 104, "amount": 50},
        {"order_id": 105, "amount": 180}
    ]
    order_list = [order["order_id"] for order in orders if order.get("amount", 0) >= 100]
    print(order_list)


if __name__ == '__main__':
    main()
