from math import log
from itertools import count
from common_utils import count_by


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


def choose_best_split_feature(dataset):
    feature_count = len(dataset[0]) - 1
    base_entropy = calc_shannon_entropy(dataset)

    def info_gain_at_axis(axis): return base_entropy - split_entropy(dataset, axis)

    info_gains = map(info_gain_at_axis, range(feature_count))

    return info_gains.index(max(info_gains))


dataset = [
    [1, 1, 'yes'],
    [1, 1, 'yes'],
    [1, 0, 'no'],
    [0, 1, 'no'],
    [0, 1, 'no']
]

# print(calc_shannon_entropy(dataset))
# print(split_dataset(dataset, 0, 1))
# print(split_dataset(dataset, 0, 0))
print(choose_best_split_feature(dataset))
