def dummy():
    pass  #this is dummy


def find_duplicates(numbers):

    # this is a dummy comment
    
    duplicates = []

    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j]:
                if numbers[i] not in duplicates:
                    duplicates.append(numbers[i])

    return duplicates
