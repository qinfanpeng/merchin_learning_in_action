from numpy import *
from common_utils import count_by


def extract_words(dataset):
    return reduce(lambda result, words: result | set(words), dataset, set([]))


def words_to_set_vector(all_words, test_words):
    return map(lambda word: 1 if word in test_words else 0, all_words)


def words_to_bag_vector(all_words, test_words):
    word_counts = count_by(lambda w: w, test_words)
    return map(lambda word: word_counts[word] if word in test_words else 0, all_words)


def train_NB(train_matrix, train_categories):
    """
     p(W|Ci) = p(W0,W1,W2...Wn|Ci) = p(W0|Ci)p(W1|Ci)p(W2|Ci)...p(Wn|Ci)
     p(Ci/W) = p(W|Ci)p(Ci) / p(W)

    """
    train_doc_count = len(train_matrix)
    word_count = len(train_matrix[0])

    p_abusive = sum(train_categories) / float(train_doc_count)  # p(Ci)

    p0_num_vector = ones(word_count)
    p1_num_vector = ones(word_count)
    p0_word_count = 2.0
    p1_word_count = 2.0

    for i in range(train_doc_count):
        if train_categories[i] == 1:
            p1_num_vector += train_matrix[i]
            p1_word_count += sum(train_matrix[i])
        else:
            p0_num_vector += train_matrix[i]
            p0_word_count += sum(train_matrix[i])

    p1_vector = log(p1_num_vector / p1_word_count)
    p0_vector = log(p0_num_vector / p0_word_count)

    """
    p(Ci/W) = p(W|Ci)p(Ci) / p(W)
    p(W|Ci) = p(W0,W1,W2...Wn|Ci) = p(W0|Ci)p(W1|Ci)p(W2|Ci)...p(Wn|Ci)
    
    p(W0|Ci)p(W1|Ci)p(W2|Ci)...p(Wn|Ci) * p(Ci)
    
    # But the product of many too small numbers will overflow, so use log
    
    log(p(W0|Ci)p(W1|Ci)p(W2|Ci)...p(Wn|Ci) * p(Ci)) = log(p(W0|Ci)) + log(p(W1|Ci)) + ... log(p(Wn|Ci)) + log(p(Ci))  
    
    """

    return p0_vector, p1_vector, p_abusive


def classify_NB(vector_to_classify, p0_vector, p1_vector, p_class1):
    # log(p(W0|Ci)p(W1|Ci)p(W2|Ci)...p(Wn|Ci) * p(Ci)) = log(p(W0|Ci)) + log(p(W1|Ci)) + ... log(p(Wn|Ci)) + log(p(Ci))

    p1 = sum(vector_to_classify * p1_vector) + log(p_class1)
    p0 = sum(vector_to_classify * p0_vector) + log(1.0 - p_class1)

    return 1 if p1 > p0 else 0


def text_parse(big_string):
    import re
    words = re.split(r'\W*', big_string)
    return [word.lower() for word in words if len(word) > 2]


def email_spam_test():
    doc_list = [];
    class_list = [];
    full_text = []

    for i in range(1, 26):
        word_list = text_parse(open('email/spam/%d.txt' % i).read())
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(1)  # Spam

        word_list = text_parse(open('email/ham/%d.txt' % i).read())
        doc_list.append(word_list)
        full_text.extend(word_list)
        class_list.append(0)  # Not spam

    vocab_list = extract_words(doc_list)  # create vocabulary
    training_set = range(50);
    test_set = []  # create test set

    for i in range(10):
        randIndex = int(random.uniform(0, len(training_set)))
        test_set.append(training_set[randIndex])
        del (training_set[randIndex])

    train_mat = [];
    train_classes = []

    for docIndex in training_set:  # train the classifier (get probs) trainNB0
        train_mat.append(words_to_bag_vector(vocab_list, doc_list[docIndex]))
        train_classes.append(class_list[docIndex])

    p0_v, p1_v, p_spam = train_NB(array(train_mat), array(train_classes))
    errorCount = 0

    for docIndex in test_set:  # classify the remaining items
        word_vector = words_to_bag_vector(vocab_list, doc_list[docIndex])
        if classify_NB(array(word_vector), p0_v, p1_v, p_spam) != class_list[docIndex]:
            errorCount += 1
            print "classification error", doc_list[docIndex]

    print 'the error rate is: ', float(errorCount) / len(test_set)


postings = [
    ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
    ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
    ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
    ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
    ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
    ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
]

class_vector = [0, 1, 0, 1, 0, 1]
words = extract_words(postings)


def testing_NB():
    posting_train_matrix = [words_to_bag_vector(words, posting) for posting in postings]
    p0_vector, p1_vector, p_abusive = train_NB(posting_train_matrix, class_vector)

    test_entry = ['love', 'my', 'dalmation']
    vector_to_class = [words_to_bag_vector(words, test_entry)]
    print test_entry, 'classified as: ', classify_NB(vector_to_class, p0_vector, p1_vector, p_abusive)

    test_entry = ['stupid', 'garbage']
    vector_to_class = [words_to_bag_vector(words, test_entry)]
    print test_entry, 'classified as: ', classify_NB(vector_to_class, p0_vector, p1_vector, p_abusive)


# print(words)
# print(words_to_vector(words, postings[0]))

# print(p0_vect)
# print(p_abusive)

# testing_NB()
email_spam_test()
