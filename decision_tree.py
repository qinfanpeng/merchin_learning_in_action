from math import log
from itertools import count
from common_utils import count_by, is_leaf
from tree_plotter import *


def calc_shannon_entropy(dataset):
    label_counts = count_by(lambda r: r[-1], dataset)

    def prop(k): return label_counts[k] / float(len(dataset))

    return reduce(lambda r, k: r - prop(k) * log(prop(k), 2), label_counts, 0.0)


def split_dataset(dataset, axis, feature):
    sub_datasets = filter(lambda features: features[axis] == feature, dataset)

    def without_feature_at_axis(feas): return [fea for (i, fea) in enumerate(feas) if i != axis]

    return map(without_feature_at_axis, sub_datasets)


def split_entropy(dataset, axis):
    feature_values = [features[axis] for features in dataset]
    feature_values = set(feature_values)

    def entropy_for_feature(feature_value):
        sub_dataset = split_dataset(dataset, axis, feature_value)
        prop = len(sub_dataset) / float(len(dataset))
        return prop * calc_shannon_entropy(sub_dataset)

    feature_entropys = map(entropy_for_feature, feature_values)
    return sum(feature_entropys)


def choose_best_split_axis(dataset):
    feature_count = len(dataset[0]) - 1
    base_entropy = calc_shannon_entropy(dataset)

    def info_gain_at_axis(axis): return base_entropy - split_entropy(dataset, axis)

    info_gains = map(info_gain_at_axis, range(feature_count))

    return info_gains.index(max(info_gains))


def majority_class(classes):
    class_counts = count_by(lambda c: c, classes)
    sorted_class_count_pairs = sorted(class_counts.items(), key=lambda k_v: k_v[1], reverse=True)
    return sorted_class_count_pairs[0][0]


def build_tree(dataset, feature_names):
    classes = [row[-1] for row in dataset]

    is_already_same_class = all([klass == classes[0] for klass in classes])
    no_feature_anymore = len(dataset[0]) == 1

    if is_already_same_class: return classes[0]
    if no_feature_anymore: return majority_class(classes)

    split_axis = choose_best_split_axis(dataset)
    split_feature_name = feature_names[split_axis]
    left_feature_names = filter(lambda feature_name: feature_name != split_feature_name, feature_names)

    tree = {split_feature_name: {}}

    feature_values = set([row[split_axis] for row in dataset])

    for feature_value in feature_values:
        tree[split_feature_name][feature_value] = build_tree(
            split_dataset(dataset, split_axis, feature_value),
            left_feature_names
        )

    return tree


def classify(tree, feature_names, test_feature_values):
    feature_name = tree.keys()[0]
    feature_index = feature_names.index(feature_name)
    feature_value = test_feature_values[feature_index]

    if is_leaf(tree[feature_name][feature_value]):
        class_label = tree[feature_name][feature_value]
    else:
        class_label = classify(tree[feature_name][feature_value], feature_names, test_feature_values)

    return class_label

def save_tree(tree, filepath):
    import pickle
    file_to_write = open(filepath, 'w')
    pickle.dump(tree, file_to_write)
    file_to_write.close()

def load_tree(filepath):
    import pickle
    file_to_read = open(filepath)

    tree = pickle.load(file_to_read)

    file_to_read.close()

    return tree


dataset = [
    [1, 1, 'yes'],
    [1, 1, 'yes'],
    [1, 0, 'no'],
    [0, 1, 'no'],
    [0, 1, 'no']
]

feature_names = ['no surfacing', 'flippers']

# print(calc_shannon_entropy(dataset))
# print(split_dataset(dataset, 0, 1))
# print(split_dataset(dataset, 0, 0))
# print(choose_best_split_axis(dataset))
# print(build_tree(dataset, feature_names))

# tree = build_tree(dataset, feature_names)
# print(tree)
# print(get_leaf_count(tree))
# print(get_tree_depth(tree))
# print(get_tree_depth({'11': 1}))
# print(create_plot(tree))
# print(classify(tree, feature_names, [1, 0]))
# save_tree(tree, 'tree_dump.txt')
# print(load_tree('tree_dump.txt'))

lenses_file = open('lenses.txt')
lenses = [line.strip().split('\t') for line in lenses_file.readlines()]
lenses_feature_names = ['age', 'prescript', 'astigmatic', 'tear_rate']
lenses_tree = build_tree(lenses, lenses_feature_names)
print(lenses_tree)
create_plot(lenses_tree)
lenses_file.close()

