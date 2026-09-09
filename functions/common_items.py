def find_common_items(list1, list2):
    common = []

    for item in list1:
        if item in list2:
            common.append(item)

    return common