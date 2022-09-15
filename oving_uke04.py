# Imports
import random
import string
import copy
import time
import numpy as np

# -------------------------------------------------------
# Assigment 1: Function for generating random string
# -------------------------------------------------------


def random_string_list(length, n_char=10):
    return [''.join(random.choices(string.ascii_lowercase, k=n_char)) for i in range(length)]


# ------------------------------
# Assigment 2: Insertion sort
# ------------------------------
def insertion_sort(unsorted_list, verbose=False):
    """ Implementation of insertion sort using lists """

    if unsorted_list:                       # Non-empty list
        # Insert single element in sorted list
        sorted_list = [unsorted_list[0]]
        n_sorted = 1                        # Counter for length of sorted list
        # Iterate over remaining unsorted items
        for item in unsorted_list[1:]:
            i = 0                           # Start comparison at index 0
            while i < n_sorted and sorted_list[i] < item:
                # Increase counter until we find a larger number, or reach end of list
                i += 1
            sorted_list.insert(i, item)      # Insert item
            n_sorted += 1                   # Increase counter for sorted items

            # (Optional:) Print progress updates
            if verbose:
                print('Inserting ' + str(item) + ' at index ' + str(i))
                print('Sorted list so far: ' + str(sorted_list))

        return sorted_list

    else:
        return unsorted_list              # If empty, return without modification


# ------------------------------------------------------
# Extra: In-place insertion sort (suitable for arrays)
# ------------------------------------------------------
def insertion_sort_inplace(unsorted_arr, verbose=False):
    """ Implementation of insertion sort "in place" (suitable for arrays) """

    # Create a copy (don't modify original list)
    arr = copy.copy(unsorted_arr)

    for i in range(1, len(arr)):           # Iterate from 1, index 0 contains single sorted item
        item = arr[i]                     # Extract item to be sorted
        j = i                             # Counter, starts at current item and works backwards
        # Continue iterating as long as item < list content at current index
        while j > 0 and item < arr[j-1]:
            arr[j] = arr[j-1]             # Copy item one step forward
            j -= 1
        arr[j] = item                     # Insert item

        if verbose:                       # (Optional:) Print progress updates
            print('Inserting item ' + str(item) + ' at index ' + str(j))
            print('[Sorted] [Unsorted]: ' +
                  str(arr[:(i+1)]) + ' ' + str(arr[i+1:]))

    return arr


# --------------------------
# Assigment 3: Merge sort
# --------------------------
def merge_sort(unsorted_list):
    """ Implementation of merge sort using lists """

    if unsorted_list:               # If non-empty list
        N = len(unsorted_list)      # Get length of list
        if N == 1:
            return unsorted_list    # Lists of length 1 are already sorted
        else:                       # N >= 2
            # Divide unsorted list into two, sort them recursively
            middle = N // 2                            # Integer division, e.g. 7 // 2 = 3
            left = merge_sort(unsorted_list[:middle])  # Left half, e.g. [0:3]
            # Right half, e.g. [3:7]
            right = merge_sort(unsorted_list[middle:])
            return merge(left, right)                   # Merge sorted lists
    else:
        return unsorted_list      # If empty, return without modification


def merge(left, right, preserve_originals=False):
    """ Merge two already sorted lists into a single sorted list. 

    Note: This method "pops" elements off lists while merging.
    It's possible to use indices to just read the input lists
    without modifying them (this method is also required for arrays). 
    However, the implementation below uses pop() because it
    demonstrates the concept nicely. 
    """

    # Optional: Make copies of input lists to avoid modifying originals
    # Not needed for merge_sort
    if preserve_originals:
        left = copy.copy(left)
        right = copy.copy(right)

    # Compare lists
    merged_list = []                            # Start with empty list
    while left and right:                       # While both lists not empty
        if left[0] < right[0]:                  # Compare first elements of sublists
            # If left[0] smallest, remove left[0] and add to merged list
            merged_list.append(left.pop(0))
        else:                                   # If right smallest,
            # If right[0] smallest, remove right[0] and add to merged list
            merged_list.append(right.pop(0))
    if left:                                    # If elements remaining in left
        # Add (already sorted) remainder of left
        merged_list += left
    else:                                       # If elements remaining in right
        # Add (already sorted) remainder of right
        merged_list += right

    return merged_list


# --------------------------------------
# Assigment 4: Measure execution time
# --------------------------------------
def sort_exp(unsorted_list, sorting_method):
    """ Experiment: Measure execution time for sorting a list

    # Inputs:
    unsorted_list:       List to be sorted, e.g. [5,3,7,1]
    sorting_method:      Sorting method, e.g. merge_sort

    # Returns:
    t_us                 Execution time in microseconds
    """
    start = time.perf_counter_ns()
    sorted_list = sorting_method(unsorted_list)
    end = time.perf_counter_ns()
    return round((end - start)/1e3)


if __name__ == "__main__":
    t_insert, t_merge, t_sorted = [], [], []
    n_list = [100, 1000, 10000]
    for n in n_list:
        unsorted_list = random_string_list(n)
        t_insert.append(sort_exp(unsorted_list, insertion_sort))
        t_merge.append(sort_exp(unsorted_list, merge_sort))
        t_sorted.append(sort_exp(unsorted_list, sorted))

    print('Execution time for sorting a list of length ' + str(n_list))
    print('Insertion sort: ' + str(t_insert) + ' us')
    print('Merge sort:     ' + str(t_merge) + ' us')
    print('sorted():       ' + str(t_sorted) + ' us')
