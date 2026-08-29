def main():
    # 请输出每个名字以及它对应的索引：
    names = ["Alice", "Bob", "Charlie", "David"]
    # enumerate → index + element
    for index, name in enumerate(names, start=1):
        print(index, name)
    print("------------------------")

    # 请找出索引为偶数（0, 2, 4...）的名字。
    names = ["Alice", "Bob", "Charlie", "David", "Eva"]
    even_names = [name for index, name in enumerate(names) if index % 2 == 0]
    print(even_names)
    print("------------------------")

    # 请生成字典 存储姓名和分数
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    students = {}
    # zip → 多个 iterable 按位置配对
    for name, score in zip(names, scores):
        students[name] = score
    # students = dict(zip(names, scores))
    print(students)
    print("-------------------------")

    # 请按照分数从高到低排序，输出：
    scores = {
        "Alice": 85,
        "Bob": 92,
        "Charlie": 78,
        "David": 95
    }
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    print(sorted_scores)
    print("--------------------------")

    # 请按照 score 从高到低对这个 list 进行排序。
    students = [
        {"name": "Alice", "score": 85},
        {"name": "Bob", "score": 92},
        {"name": "Charlie", "score": 78},
        {"name": "David", "score": 95}
    ]
    sorted_list = sorted(students, key=lambda student: student["score"], reverse=True)
    print(sorted_list)
    print("--------------------------")

    # score 从高到低; 如果 score 相同，则 age 从小到大
    students = [
        {"name": "Alice", "age": 25, "score": 90},
        {"name": "Bob", "age": 22, "score": 90},
        {"name": "Charlie", "age": 25, "score": 85},
        {"name": "David", "age": 22, "score": 95}
    ]
    sorted_list = sorted(
                     students,
                     key=lambda student: (-student["score"], student["age"]))
    print(sorted_list)
    print("--------------------------")

    # 去除重复元素，同时保持原来的顺序。
    numbers = [1, 2, 3, 2, 5, 1, 4, 3, 6]
    distinct_numbers = []
    seen = set()
    for number in numbers:
        if number not in seen:
            seen.add(number)
            distinct_numbers.append(number)
    print(distinct_numbers)
    print("--------------------------")

    # 请统计每个城市有多少用户。
    users = [
        {"name": "Alice", "city": "Beijing"},
        {"name": "Bob", "city": "Shanghai"},
        {"name": "Charlie", "city": "Beijing"},
        {"name": "David", "city": "Shanghai"},
        {"name": "Eva", "city": "Beijing"}
    ]
    city_count = {}
    for user in users:
        city_count[user["city"]] = city_count.get(user["city"], 0) + 1
    print(city_count)
    print("--------------------------")




if __name__ == "__main__":
    main()
