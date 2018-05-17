def count_by(f, collection):
    count_dict = {}
    for value in collection:
        key = f(value)
        count_dict[key] = count_dict.get(key, 0) + 1

    return count_dict
