from collections import Counter


def get_top_k_frequent(nums, k):
    freq = Counter(nums)
    print(freq)
    print(freq.most_common(k))
    return [item[0] for item in freq.most_common(k)]

def main():
    nums = ['a', 'a', 'c', 'e', 'c', 'd', 'e', 'e', 'b', 'a']
    top_k = get_top_k_frequent(nums, 3)

    print(top_k)


if __name__ == '__main__':
    main()