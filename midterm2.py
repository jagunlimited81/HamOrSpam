# Authors
#   - Jared Tremlbey
#   - Kaleb
import random
import os


class MVBEM:
    def __init__(self, train, test):
        # split data into words
        self.train_data = [(a, b.split(" ")) for a, b in train]
        # print(self.train_data[0])
        self.test_data = [(a, b.split(" ")) for a, b in test]

        # split into labels
        self.train_data_ham = [_ for label,
                               _ in self.train_data if label == "ham"]
        self.train_data_spam = [_ for label,
                                _ in self.train_data if label == "spam"]

        # print(self.train_data_spam[0])
        # get the number of total words
        self.len_ham = sum([len(l) for l in self.train_data_ham])
        self.len_spam = sum([len(l) for l in self.train_data_spam])

        # Create Vocabulary
        self.vocabulary = []
        for label, data in self.test_data:
            for word in data:
                self.vocabulary.append(word)
        self.vocabulary = list(set(self.vocabulary))
        self.len_vocabulary = len(self.vocabulary)

        self.wordCountsHam = {}
        self.wordCountsSpam = {}
        for word in self.vocabulary:
            self.wordCountsHam[word] = sum(
                [1 for i in self.train_data_ham if word in i])
            self.wordCountsSpam[word] = sum(
                [1 for i in self.train_data_spam if word in i])

        # Initiate parameters
        self.parameters_spam = {
            unique_word: 0 for unique_word in self.vocabulary}
        self.parameters_ham = {
            unique_word: 0 for unique_word in self.vocabulary}

        alpha = 1

        # Calculate parameters
        for word in self.vocabulary:
            # sum up all occurences of the word

            # spam_messages already defined
            self.n_word_given_spam = self.wordCountsSpam[word]
            self.p_word_given_spam = (
                self.n_word_given_spam + alpha) / (self.len_spam + alpha*self.len_vocabulary)
            self.parameters_spam[word] = self.p_word_given_spam

            # ham_messages already defined
            self.n_word_given_ham = self.wordCountsHam[word]
            self.p_word_given_ham = (
                self.n_word_given_ham + alpha) / (self.len_ham + alpha*self.len_vocabulary)
            self.parameters_ham[word] = self.p_word_given_ham

    def hamOrSpam(self, email: str) -> str:
        email = email.split(' ')

        p_ham = .5
        p_spam = .5
        for word in email:
            if word in self.parameters_spam:
                p_spam *= self.parameters_spam[word]
            if word in self.parameters_ham:
                p_ham *= self.parameters_ham[word]
            while p_spam < 1/100 and p_ham < 1/100:
                p_spam = p_spam * 10
                p_ham = p_ham * 10
        if p_ham > p_spam:
            return "ham"
        elif p_ham < p_spam:
            return "spam"
        else:
            print("There was a tie")
            return "tie"


def load_datasets():
    # set data paths
    data_folder = os.path.join("email data")
    ham_folders = [
        os.path.join(data_folder, "Ham", "300 good emails"),
        os.path.join(data_folder, "Ham", "301-600 good ones")
    ]
    spam_folders = [os.path.join(data_folder, "Spam")]

    # Create a list from 1-600
    numbers = list(range(1, 601))

    # Shuffle the list and splice it to create the dataset
    random.shuffle(numbers)
    ham_training_num = numbers[0:500:]
    ham_test_num = numbers[500:]

    random.shuffle(numbers)
    spam_training_num = numbers[0:500:]
    spam_test_num = numbers[500:]

    # data is a list of tuples (Ham or Spam , email data)
    training_data = []
    test_data = []

    # load the spam training data
    for i in spam_training_num:
        f = open(os.path.join(spam_folders[0], f"{i}.txt"), "r")
        data = f.read()
        f.close()
        training_data.append(("spam", data))

    # load the spam test data
    for i in spam_test_num:
        f = open(os.path.join(spam_folders[0], f"{i}.txt"), "r")
        data = f.read()
        f.close()
        test_data.append(("spam", data))

    # load the ham training data
    for i in ham_training_num:
        f = open(os.path.join(
            ham_folders[0 if i <= 300 else 1],
            f"{i if i <= 300 else i-300}.txt"),
            "r")
        data = f.read()
        f.close()
        training_data.append(("ham", data))

    # load the ham test data
    for i in ham_test_num:
        f = open(os.path.join(
            ham_folders[0 if i <= 300 else 1],
            f"{i if i <= 300 else i-300}.txt"),
            "r")
        data = f.read()
        f.close()
        test_data.append(("ham", data))

    # clean the data
    training_data = [(d, data.strip(" \n")) for d, data in training_data]
    test_data = [(d, data.strip(" \n")) for d, data in test_data]
    return (training_data, test_data)


def main():
    print("\nreading data from files...")
    train, test = load_datasets()

    print("\ncreating model...")
    model = MVBEM(train, test)

    print("\ntesting model...")
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for answer, email in test:
        model_answer = model.hamOrSpam(email)

        # If we got the correct answer, TRUE answers only
        if model_answer == answer:
            if model_answer == "spam":
                true_positive += 1
            elif model_answer == "ham":
                true_negative += 1
        
        else:
            if model_answer == "spam":
                false_positive += 1
            elif model_answer == "ham":
                false_negative += 1

    print("\nResults:")
    print(f"  true positives: {true_positive}")
    print(f"  false negatives: {false_negative}")
    print(f"  true negatives: {true_negative}")
    print(f"  false positives: {false_positive}")
    print()

    precision = true_positive/(true_positive + false_positive)
    recall = true_positive/(true_positive + false_negative)
    f1 = 2 * ((precision * recall) / (precision + recall))
    accuracy = (true_positive + true_negative) / len(test)

    print("Statistics:")
    print(f"  Precision: {precision}")
    print(f"  Recall: {recall}")
    print(f"  F1: {f1}")
    print(f"  Accuracy: {accuracy}")
    print()


if __name__ == "__main__":
    main()
