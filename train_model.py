### HW_2 ### 
### NLP  ###
### Trafalis Panagiotis ###
### Ioannis Fitsopoulos ###
### Eirini Nomikou ###


from nltk import bigrams,trigrams
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
import pickle
import math


def first_exe():
    import nltk
    nltk.download('punkt')


def model_train():
    filename = 'big.txt'
    lang_model = LanguageModel(filename)

class LanguageModel:
    def __init__(self, filename):
        text = open(filename, 'r').read()

        # List with sentences
        self.sentences = [sentence for sentence in sent_tokenize(text)]

        # Define models
        self.model = defaultdict(lambda: defaultdict(lambda: 0))
        self.model_bigrams = defaultdict(lambda: defaultdict(lambda: 0))
        self.model_unigrams = defaultdict(lambda:0)

        # Counters
        self.totals = 0
        self.totals_bigrams = 0
        self.total_unigram = 0

        self.trigrams_()
        self.bigrams_()
        self.unigrams_()

        self.convert_to_pct()

        # Set default dicts to dicts
        self.model = dict(self.model)
        self.model_bigrams = dict(self.model_bigrams)
        # self.model_unigrams = dict()

        # Save models
        pickle.dump(self.model, open('models/trigram_model.p', 'wb'))
        pickle.dump(self.model_bigrams, open('models/bigram_model.p', 'wb'))
        pickle.dump(self.model_unigrams, open('models/unigram_model.p', 'wb'))



    def trigrams_(self):

        for sentence in self.sentences:
            words = word_tokenize(sentence)
            for w1, w2, w3 in trigrams(words, pad_right=True, pad_left=True):
                w1 = str(w1).lower()
                w2 = str(w2).lower()
                w3 = str(w3).lower()
                self.model[(w1, w2)][w3] += 1
                self.totals += 1


    def bigrams_(self):

        for sentence in self.sentences:
            words = word_tokenize(sentence)
            for w1, w2 in bigrams(words, pad_right=True, pad_left=True):
                w1 = str(w1).lower()
                w2 = str(w2).lower()
                
                self.model_bigrams[w1][w2] += 1
                self.totals_bigrams += 1

    def unigrams_(self):

        for sentence in self.sentences:
            words = word_tokenize(sentence)
            for w1 in words:
                self.model_unigrams[w1] +=1
                self.total_unigram +=1

    def convert_to_pct(self):


        # Sort Dict
        for key, value in self.model.items():
            self.model[key] = dict(sorted(value.items(), key=lambda x: x[1], reverse=True))

        for key, value in self.model_bigrams.items():
            self.model_bigrams[key] = dict(sorted(value.items(), key=lambda x: x[1], reverse=True))

        self.model_unigrams = dict(self.model_unigrams)

        self.model_unigrams = dict(sorted(self.model_unigrams.items(), key=lambda x: x[1], reverse=True))
        


if __name__ == '__main__':
    import setup
    # Stand alone test
    # first_exe()

    # In the first usage uncomment the following function to train the model
    model_train()
