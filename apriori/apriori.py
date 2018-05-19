# coding=utf-8
from common_utils import count_by, identity, flatten, paris_in
from itertools import combinations, permutations

import numpy as np

def create_C1(dataset):
    C1 = [[item] for item in set(items_of_dataset(dataset))]
    C1.sort()

    return C1

def create_Ck(Lk_1, k):  # L1 -> C2
    unique_l_items = set(flatten(Lk_1))
    candidates = map(list, list(combinations(unique_l_items, k)))

    def all_subset_is_in_lk_1(c_items):       # e.g. all subset of C2 should in L1
        c_item_subsets = map(list, list(combinations(c_items, k - 1)))
        return all(map(lambda subset: subset in Lk_1, c_item_subsets))

    return filter(all_subset_is_in_lk_1, candidates)

    # ret_list = []
    # for i in range(len(Lk_1)):
    #     for j in range(i + 1, len(Lk_1)):
    #         L1 = list(Lk_1[i])[:k-2]
    #         L2 = list(Lk_1[j])[:k-2]
    #         L1.sort()
    #         L2.sort()
    #         if L1 == L2:  # if first k-2 elements are equal
    #             ret_list.append(set(Lk_1[i]) | set(Lk_1[j]))  # set union
    #
    # return map(list, ret_list)


def items_of_dataset(dataset):
    return [
        item
        for transaction in dataset
        for item in transaction
    ]


def scan_D(D, Ck, min_support):
    matched_c_items = [
        c
        for row in D
        for c in Ck if set(c).issubset(set(row))
    ]

    matched_c_items = map(frozenset, matched_c_items)
    item_counts = count_by(identity, matched_c_items)

    def support(item): return item_counts[item] / float(len(D))

    Lk = list(set(
        filter(lambda item: support(item) >= min_support, matched_c_items)
    ))

    support_data = {item: support(item) for item in Lk}

    return map(list, Lk), support_data


def apriori(dataset, min_support=0.5):
    C1 = create_C1(dataset)
    L1, support_data = scan_D(dataset, C1, min_support)
    L = [L1]
    k = 2

    print('C1: ' + str(C1))
    print('L1: ' + str(L1))

    while len(L[k-2]) > 0:
        Ck = create_Ck(L[k-2], k)
        Lk, support_data_k = scan_D(dataset, Ck, min_support)

        if len(Ck) > 0:
            print('C' + str(k) + ': ' + str(Ck))
            print('L' + str(k) + ': ' + str(Lk))

        L.append(Lk)
        support_data.update(support_data_k)
        k += 1

    print('support_data: ' + str(support_data))
    return L, support_data

def generate_rules(L, support_data, min_conf=0.7):
    possible_rules = []
    for i in range(1, len(L)):    # Only L2+ may have rule like a -> b
        for frequent_items in L[i]:
            rules = paris_in(frequent_items)

            possible_rules.extend(rules)
            reversed_rules = map(tuple, map(reversed, rules))
            possible_rules.extend(reversed_rules)

    matched_rules = filter(lambda r: confidence(r, support_data) >= min_conf, possible_rules)

    for rule in matched_rules:
        print(str(rule[0]) + '->' + str(rule[1]) + ' conf: ' + str(confidence(rule, support_data)))

    return matched_rules


def confidence(rule, support_data):
    # confidence(a->b) = support(ab) / support(a)
    left = rule[0]
    frequent_items = flatten(rule)

    return support_data[frozenset(frequent_items)] / support_data[frozenset(left)]


dataset = [
    [1, 3, 4],
    [2, 3, 5],
    [1, 2, 3, 5],
    [2, 5]
]

# print(create_C1(dataset))
# C1 = create_C1(dataset)
# L1, support_data1 = scan_D(dataset, C1, 0.5)
# print('C1: ' + str(C1))
# print('L1: ' + str(L1))
# print('support_data1: ' + str(support_data1))
L, support_data = apriori(dataset, min_support=0.5)
rules = generate_rules(L, support_data, min_conf=0.7)
