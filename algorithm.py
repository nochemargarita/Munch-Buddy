"""Algorithm"""
from math import sqrt

def pearson(pairs):
    """Return Pearson correlation for pairs. -1..1"""

    series_1, series_2 = zip(*pairs)

    sum_1 = sum(series_1)
    sum_2 = sum(series_2)

    squares_1 = sum([n * n for n in series_1])
    squares_2 = sum([n * n for n in series_2])

    product_sum = sum([n * m for n, m in pairs])

    size = len(pairs)

    numerator = product_sum - ((sum_1 * sum_2) / size)

    denominator = sqrt((squares_1 - (sum_1 ** 2) / size) *
                  (squares_2 - (sum_2 ** 2) / size))

    return numerator / denominator



# class Pearson(object):

#     def pearson(pairs):
#         """Return Pearson correlation for pairs. -1..1"""

#         series_1, series_2 = zip(*pairs)

#         sum_1 = sum(series_1)
#         sum_2 = sum(series_2)

#         squares_1 = sum([n * n for n in series_1])
#         squares_2 = sum([n * n for n in series_2])

#         product_sum = sum([n * m for n, m in pairs])

#         size = len(pairs)

#         numerator = product_sum - ((sum_1 * sum_2) / size)

#         denominator = sqrt((squares_1 - (sum_1 ** 2) / size) *
#                       (squares_2 - (sum_2 ** 2) / size))

#         return numerator / denominator