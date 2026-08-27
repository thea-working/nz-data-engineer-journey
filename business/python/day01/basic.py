import operator


def main():
    # Q1:统计列表中偶数的数量
    numbers = [1, 4, 7, 10, 13, 16, 20, 25]

    result = 0
    for num in numbers:
        if num % 2 == 0:
            result += 1

    print(result)
    print('--------------')

    even_number = sum(1 for num in numbers if num % 2 == 0)
    print(even_number)
    print('--------------')

    # Q2:找出列表中的最大值。
    numbers = [12, 45, 7, 89, 23, 56, 34]
    if not numbers:
        print('list is empty')
    else:
        max_val = numbers[0]
        for num in numbers:
            if num > max_val:
                max_val = num
        print(max_val)
    print('--------------')

    # Q3:统计列表中每个数字出现的次数
    numbers = [1, 2, 2, 3, 1, 4, 2, 3, 5, 1]
    num_count = {}
    for num in numbers:
        if num in num_count:
            num_count[num] += 1
        else:
            num_count[num] = 1
        # num_count[num] = num_count.get(num,0) + 1
    print(num_count)
    print('--------------')

    # Q5:出现次数最多的数字
    numbers = [4, 7, 2, 7, 4, 9, 2, 7, 5]
    num_count = {}
    for num in numbers:
        num_count[num] = num_count.get(num, 0) + 1
    if not num_count:
        print('list is empty')
    else:
        max_num = next(iter(num_count.keys()))
        max_count = num_count[max_num]
        for num in num_count:
            if num_count[num] > max_count:
                max_count = num_count[num]
                max_num = num
        print(max_num)
    print('--------------')

    # Q5: 去除列表中的重复元素
    numbers = [1, 2, 2, 3, 4, 3, 5, 1, 6]
    distinct_numbers = []
    for num in numbers:
        if num not in distinct_numbers:
            distinct_numbers.append(num)
    print(distinct_numbers)
    print('--------------')

    # Q6: 找出列表中的第二大的不同数字
    numbers = [10, 5, 18, 20, 15, 20, 3]
    largest = float('-inf')
    second_largest = float('-inf')
    for num in numbers:
        if num > largest:
            second_largest = largest
            largest = num
        elif largest > num > second_largest:
            second_largest = num

    print(largest)
    print(second_largest)
    print('--------------')

    # Q7: 字符串中每个字符出现的次数
    text = "dataengineer"
    ch_count = {}
    for ch in text:
        ch_count[ch] = ch_count.get(ch, 0) + 1
    print(ch_count)
    print('--------------')

    # Q8: 找出第一个不重复的字符(第一个只出现一次的字符)
    text = "aabbcddeff"
    ch_count = {}
    for ch in text:
        ch_count[ch] = ch_count.get(ch, 0) + 1
    result = None
    for ch in text:
        if ch_count.get(ch) == 1:
            result = ch
            break
    print(result)
    print('--------------')

    # Q9: 列表中找出所有大于平均值的数字
    numbers = [10, 20, 30, 40, 50]
    avg_val = sum(numbers) / len(numbers)
    result = []
    for num in numbers:
        if num > avg_val:
            result.append(num)
    # result = [num for num in numbers if num > avg_val]
    print(result)
    print('--------------')

    # Q10: 判断一个字符串是否是回文字符串（Palindrome）
    # 如果一个字符串从左往右和从右往左完全一样，就叫 palindrome。
    text = "hello"
    i = 0
    j = len(text) - 1
    flag = True
    while i < j:
        if text[i] != text[j]:
            flag = False
            break

        i += 1
        j -= 1

    print(flag)


if __name__ == '__main__':
    main()
