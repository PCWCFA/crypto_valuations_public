
def search(list, val):
    first = -1
    last = len(list)
    index = -2

    while (first <= last) and (index == -2):
        mid = (first+last)//2

        if list[mid] == val:
            index = mid
        elif first+1 == last and index == -2:
            return index
        else:
            if val < list[mid]:
                last = mid
            else:
                first = mid

    return index
