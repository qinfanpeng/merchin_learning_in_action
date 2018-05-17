from numpy import *
import matplotlib
import matplotlib.pyplot as plt
from os import listdir

from common_utils import count_by

def classify0(to_test_matrix, training_matrix, labels, k):
    training_count = training_matrix.shape[0]
    input_matrix = tile(to_test_matrix, (training_count, 1))

    distances = distances_of_two_matrixes(input_matrix, training_matrix)
    sorted_distance_indices = distances.argsort()
    top_k_distance_indices = sorted_distance_indices[:k]
    label_count_dict = count_by(lambda i: labels[i], top_k_distance_indices)
    sorted_label_count_pairs = sorted(label_count_dict.items(), key=lambda k_v: k_v[1], reverse=True)

    return sorted_label_count_pairs[0][0]


def distances_of_two_matrixes(matrix1, matrix2):
    distance_matrix = matrix1 - matrix2
    sqrt_distance_matrix = distance_matrix ** 2
    sum_of_sqrt_distance_matrix = sqrt_distance_matrix.sum(axis=1)

    return sum_of_sqrt_distance_matrix ** 0.5


def file_to_matrix(filename):
    lines = open(filename).readlines()
    lines_count = len(lines)
    dataset_matrix = zeros((lines_count, 3))

    label_vector = []

    for index, line in enumerate(lines):
        striped_line = line.strip()
        features = striped_line.split('\t')

        dataset_matrix[index, :] = features[0:3]
        label_vector.append(int(features[-1]))

    return dataset_matrix, label_vector


def img_to_vector(filename):
    vector = zeros((1, 1024))
    file = open(filename)

    for i in range(32):
        line = file.readline()
        for j in range(32):
            vector[0, 32 * i + j] = int(line[j])

    return vector


# vector = img_to_vector('digits/testDigits/0_0.txt')
# print(vector[0, 0:31])
# print(vector[0, 32:64])


def normalize(matrix):
    """
    (origin_value - min) / (max - min)
    """

    mins = matrix.min(0)
    maxs = matrix.max(0)
    ranges = maxs - mins

    matrix_row_count = matrix.shape[0]
    normalized_matrix = (matrix - tile(mins, (matrix_row_count, 1))) / tile(ranges, (matrix_row_count, 1))

    return normalized_matrix, ranges, mins


dating_matrix, dating_labels = file_to_matrix('datingTestSet2.txt')

figure = plt.figure()
ax = figure.add_subplot(111)
ax.scatter(dating_matrix[:, 1], dating_matrix[:, 2], 15.0 * array(dating_labels), 15.0 * array(dating_labels))
# plt.show()

normalized_dating_matrix, ranges, mins = normalize(dating_matrix)

# print(normalized_dating_matrix[0:4, :])
# print(ranges)
# print(mins)

def _not(func):
    def not_func(*args, **kwargs):
        return not func(*args, **kwargs)

    return not_func


def dating_class_test():
    dating_matrix, dating_labels = file_to_matrix('datingTestSet2.txt')
    normalized_matrix, _ranges, _mins = normalize(dating_matrix)
    matrix_row_count = normalized_matrix.shape[0]

    test_ratio = 0.10
    test_count = int(matrix_row_count * test_ratio)

    def is_class_correctly(i):
        class_result = classify0(normalized_matrix[i, :], normalized_matrix[test_count:matrix_row_count, :],
                                 dating_labels[test_count:matrix_row_count], 3)
        return class_result == dating_labels[i]

    # error_count = len(filter(lambda i: not is_class_correctly(i), range(test_count)))
    error_count = len(filter(_not(is_class_correctly), range(test_count)))

    print("total error rate is: %f" % (error_count / float(test_count)))

def hand_writing_class_test():
    hand_write_labels = []
    training_path = 'digits/trainingDigits'
    test_path = 'digits/testDigits'
    training_file_list = listdir(training_path)
    test_file_list = listdir(test_path)
    training_count = len(training_file_list)
    test_count = len(test_file_list)
    training_matrix = zeros((training_count, 1024))

    for i in range(training_count):
        filename = training_file_list[i]
        number_label = int(filename.split('.')[0].split('_')[0])  # filename e.g 2_4.txt

        hand_write_labels.append(number_label)
        training_matrix[i, :] = img_to_vector(training_path + '/' + filename)

    error_count = 0.0

    for i in range(test_count):
        filename = test_file_list[i]
        number_label = int(filename.split('.')[0].split('_')[0])  # filename e.g 2_4.txt

        vector_to_test = img_to_vector(training_path + '/' + filename)
        class_result = classify0(vector_to_test, training_matrix, hand_write_labels, 3)

        print('The classify result is: %d, the real answer is: %d' % (class_result, number_label))

        if class_result != number_label:
            error_count += 1

    print('total error rate is: %f' % (error_count / float(test_count)))

dating_class_test()
# hand_writing_class_test()
