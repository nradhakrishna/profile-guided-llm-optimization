import cProfile

from functions.duplicates import find_duplicates
from functions.sentence import create_sentence
from functions.common_items import find_common_items


numbers = list(range(10000))
words = ["hello"] * 100000
list1 = list(range(10000))
list2 = list(range(5000, 15000))


def run_tests():
    find_duplicates(numbers)
    create_sentence(words)
    find_common_items(list1, list2)


profiler = cProfile.Profile()

run_tests()


# for stat in stats:
#     print(stat)