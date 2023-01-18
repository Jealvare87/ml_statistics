# --------------------------------------------
# IMPORTS
# --------------------------------------------

import numpy as np
import pandas as pnd
import matplotlib.pyplot as plt
import math


# --------------------------------------------
# FUNCTIONS
# --------------------------------------------

def calc_minimum_maximum(observations):
    sorted_list = observations.sort_values(by="NOTAS", axis=0)
    sorted_list = sorted_list.reset_index(drop=True)
    return sorted_list['NOTAS'][0], sorted_list['NOTAS'][len(sorted_list) - 1]


def arithmetic_average(observations):
    values = observations['NOTAS']
    n = values.count()
    average, total_avg = 0, 0

    if n > 0:
        for val in values:
            average += val
        total_avg = average / n

    return total_avg


def calc_median(observations):
    sorted_list = observations.sort_values(by="NOTAS", axis=0)
    sorted_list = sorted_list.reset_index(drop=True)
    n = observations['NOTAS'].count()
    half = math.trunc(n / 2) - 1

    if n % 2 == 1:
        half += 1
        return sorted_list['NOTAS'][half]
    else:
        offset = sorted_list['NOTAS'][half + 1] - sorted_list['NOTAS'][half]
        median = sorted_list['NOTAS'][half] + offset
        return median


def count_mode(observations):
    values = observations['NOTAS']
    dictionary = {}
    s_dictionary = {}
    # Initialize
    for val in values:
        dictionary[val] = 0

    # Count
    for val in values:
        if val in dictionary:
            dictionary[val] += 1

    # Sort
    for val in sorted(dictionary, key=dictionary.get, reverse=True):
        s_dictionary[val] = dictionary[val]

    return s_dictionary


def calc_variance(observations, n, average):
    variance = 0
    values = observations['NOTAS']
    for val in values:
        variance += (val - average) ** 2
    return variance / (n - 1)


def calc_quartiles(observations, n):
    q1, q2, q3 = round(n / 4) - 1, round(n / 2) - 1, round((n * 3) / 4) - 1
    sorted_values = observations.sort_values(by=['NOTAS'], axis=0)
    sorted_values = sorted_values.reset_index(drop=True)
    values = list(sorted_values['NOTAS'])

    val_q1 = (values[q1] + ((values[q1 + 1] - values[q1]) / 2) + values[q1 + 1]) / 2 if q1 % 2 == 1 else values[q1]
    val_q2 = (values[q2] + ((values[q2 + 1] - values[q2]) / 2) + values[q2 + 1]) / 2 if q2 % 2 == 1 else values[q2]
    val_q3 = (values[q3] + ((values[q3 + 1] - values[q3]) / 2) + values[q3 + 1]) / 2 if q3 % 2 == 1 else values[q3]

    return val_q1, val_q2, val_q3


def calc_turkey_criteria(observations, q1, q3):
    lower_limit_values = []
    upper_limit_values = []
    observ = observations.sort_values(by=['NOTAS'], axis=0)
    inter_quartile = q3 - q1

    lower_limit = q1 - (1.5 * inter_quartile)
    upper_limit = q3 + (1.5 * inter_quartile)

    for value in np.nditer(observ.values):
        # turn 2-D array to 1-D by first element
        value = value.flat[0]
        if value < lower_limit:
            lower_limit_values.append(value)
        if value > upper_limit:
            upper_limit_values.append(value)

    limit_values = lower_limit_values + upper_limit_values

    return limit_values


def visualize(observations, average, median, q1, q2, q3):
    # Average
    plt.subplot(2, 2, 1)
    plt.hist(observations)
    plt.title("Histogram an average")
    plt.axvline(average, color="red", linestyle="dashed", linewidth=1, label=str(average))
    plt.legend(loc="upper right")

    # Median
    plt.subplot(2, 2, 2)
    plt.hist(observations)
    plt.title("Histogram an median")
    plt.axvline(median, color="green", linestyle="dashed", linewidth=1, label=str(median))
    plt.legend(loc="upper right")

    # Quartiles
    plt.subplot(2, 2, 3)
    plt.hist(observations)
    plt.title("Histogram and quartiles")
    plt.axvline(q1, color="orange", linestyle="dashed", linewidth=1, label="Q1: " + str(q1))
    plt.axvline(q2, color="orange", linestyle="dashed", linewidth=1, label="Q2: " + str(q2))
    plt.axvline(q3, color="orange", linestyle="dashed", linewidth=1, label="Q3: " + str(q3))
    plt.legend(loc="upper right")

    # Diagram
    plt.subplot(2, 2, 4)
    plt.boxplot(observations)
    plt.title("Box-and-whisker diagram")
    plt.show()


# --------------------------------------------
# APPLICATION
# --------------------------------------------


obs = pnd.DataFrame({"NOTAS": np.array([3, 19, 10, 15, 14, 12, 9, 8, 11, 12, 11, 12, 13, 11, 14, 16])})
features = obs.size
minimum, maximum = calc_minimum_maximum(obs)
avg = arithmetic_average(obs)
mdn = calc_median(obs)
sorted_mode = count_mode(obs)
first_element = list(sorted_mode.values())[0]
# result = dict(((v, k) for k in mydict for v in mydict[k] if v in required))
list_mode = list(k for k in list(sorted_mode.keys()) if sorted_mode.get(k) == first_element)
var = calc_variance(obs, features, avg)
average_deviation = math.sqrt(var)
quart = calc_quartiles(obs, int(features))
turkey = calc_turkey_criteria(obs, quart[0], quart[2])

# Print results
print(str(obs))
print("-----------------------------")
print("Count    = " + str(features))
print("Min      = " + str(minimum))
print("Max      = " + str(maximum))
print("Range    = " + str(maximum - minimum))
print("Average  = " + str(avg))
print("Median   = " + str(mdn))
print('Mode     = ' + str(list_mode))
print('Variance = ' + str(var))
print('Dev.     = ' + str(round(average_deviation, 2)))
print("-----------------------------")
print("25% of the observations have a grade lower than " + str(quart[0]))
print("50% of the observations have a grade around " + str(quart[1]))
print("75% of the observations have a grade lower than " + str(quart[2]))
print("The grades of the lowest 25% differ from those of the highest 25% by " + str(quart[2] - quart[0]) + " points")
print("Turkey values are " + str(turkey))

visualize(obs, avg, mdn, quart[0], quart[1], quart[2])
