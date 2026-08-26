

def merge_sorted_list(a,b):
    """Merge two sorted lists."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else :
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

def main():
    a = [2, 6, 9, 11, 19]
    b = [4, 5, 12, 16, 21, 27]
    result = merge_sorted_list(a,b)
    print(result)

if __name__ == '__main__':
    main()
