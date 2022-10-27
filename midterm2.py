# Authors
#   - Jared Tremlbey
#   - Kaleb
import random
import os


class MVBEM:
    def __init__(self, train, test):
        # split data into words
        self.train_data = [(a, b.split(" ")) for a, b in train]
        print(self.train_data[0])
        self.test_data = [(a, b.split(" ")) for a, b in test]
        self.vocabulary = []

        # split into labels
        self.train_data_ham = [_ for label, _ in self.train_data if label == "ham"]
        self.train_data_spam = [_ for label, _ in self.train_data if label == "spam"]

        print(self.train_data_spam[0])

        self.len_ham = len(self.train_data_ham)
        self.len_spam = len(self.train_data_spam)

        # Create Vocabulary
        for label, data in self.test_data:
            for word in data:
                self.vocabulary.append(word)
        self.vocabulary = list(set(self.vocabulary))
        self.len_vocabulary = len(self.vocabulary)

        self.wordCountsHam = {}
        self.wordCountsSpam = {}
        for word in self.vocabulary:
            self.wordCountsHam[word] = sum([1 for i in self.wordCountsHam if word in i])
            self.wordCountsSpam[word] = sum([1 for i in self.wordCountsSpam if word in i])
        # Initiate parameters
        self.parameters_spam = {unique_word:0 for unique_word in self.vocabulary}
        self.parameters_ham = {unique_word:0 for unique_word in self.vocabulary}

        alpha = 1

        # Calculate parameters
        for word in self.vocabulary:
            # sum up all occurences of the word 

            self.n_word_given_spam = self.wordCountsSpam[word] # spam_messages already defined
            self.p_word_given_spam = (self.n_word_given_spam + alpha) / (self.len_spam + alpha*self.len_vocabulary)
            self.parameters_spam[word] = self.p_word_given_spam

            self.n_word_given_ham = self.wordCountsHam[word] # ham_messages already defined
            self.p_word_given_ham = (self.n_word_given_ham + alpha) / (self.len_ham + alpha*self.len_vocabulary)
            self.parameters_ham[word] = self.p_word_given_ham

    def hamOrSpam(self, email: str) -> str:
        email = email.split(' ')
        # https://www.kdnuggets.com/2020/07/spam-filter-python-naive-bayes-scratch.html#:~:text=Classifying%20A%20New%20Message 
        p_ham = .5
        p_spam = .5

        for word in email:
            if word in self.parameters_spam:
                print("here")
                p_spam *= self.parameters_spam[word]
            if word in self.parameters_ham:
                p_ham *= self.parameters_ham[word]
        
        print(p_ham)
        print(p_spam)
        return "ham"


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
    
    model.hamOrSpam("")


if __name__ == "__main__":
    main()
