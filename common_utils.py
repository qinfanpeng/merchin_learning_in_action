# coding=utf-8
def count_by(f, collection):
    def update_count(count_dict, item):
        key = f(item)
        count_dict[key] = count_dict.get(key, 0) + 1
        return count_dict

    return reduce(update_count, collection, {})


def identity(x): return x


def is_leaf(tree_node):
    return not isinstance(tree_node, dict)


def flatten(nest_list):
    return [
        item
        for sub_list in nest_list
        for item in sub_list
    ]


def without(collection, value):
    if isinstance(value, list):
        return list(set(collection) - set(value))
    else:
        return [item for item in collection if item != value]


def paris_in(list):
    """
    A ⟶ B
     ↖︎  ↙︎
       C
    随机把 [A, B, C] 拆分成两份，将其想象成循环链表
    """
    max_pair_side_length = len(list) / 2
    return [
        (list[i:i + pair_size], without(list, list[i:i + pair_size]))
        for i in range(len(list))
        for pair_size in range(1, max_pair_side_length + 1)
    ]
