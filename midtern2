# Authors
#   - Jared Tremlbey
#   - Kaleb
import random
import os


class MVBEM:
    def __init__(self, train, test):
        self.train_data = train
        self.test_data = test
        self.vocabulary = []
        for classification, data in self.test_data:
            for word in data:
                self.vocabulary.append(word)
        self.vocabulary = list(set(self.vocabulary))

    def train(self, ):
        pass

    def hamOrSpam(self, email) -> str:
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

    model.train()
    
    model.hamOrSpam("asdf")


if __name__ == "__main__":
    main()
