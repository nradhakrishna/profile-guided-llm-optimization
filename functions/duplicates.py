def dummy():
    pass  #this is dummy


def find_duplicates(numbers):
    seen_hashable = set()
    dup_hashable = set()
    seen_unhashable = []
    duplicates = []

    for item in numbers:
        try:
            if item in seen_hashable:
                if item not in dup_hashable:
                    dup_hashable.add(item)
                    duplicates.append(item)
            else:
                seen_hashable.add(item)
        except TypeError:
            # Fallback for unhashable objects (e.g., lists, dicts)
            if any(item == existing for existing in seen_unhashable):
                if not any(item == existing for existing in duplicates):
                    duplicates.append(item)
            else:
                seen_unhashable.append(item)

    return duplicates
