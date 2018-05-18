def count_by(f, collection):
    def update_count(count_dict, item):
        key = f(item)
        count_dict[key] = count_dict.get(key, 0) + 1
        return count_dict

    return reduce(update_count, collection, {})

def is_leaf(tree_node):
    return not isinstance(tree_node, dict)