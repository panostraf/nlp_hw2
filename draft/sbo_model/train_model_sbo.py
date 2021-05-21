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

        # self.trigrams_()
        self.bigrams_()
        self.unigrams_()

        self.convert_to_pct()

        # # Set default dicts to dicts
        # self.model = dict(self.model)
        # self.model_bigrams = dict(self.model_bigrams)
        # # self.model_unigrams = dict()

        # # Save models
        # pickle.dump(self.model, open('models/trigram_model.p', 'wb'))
        # pickle.dump(self.model_bigrams, open('models/bigram_model.p', 'wb'))
        # pickle.dump(self.model_unigrams, open('models/unigram_model.p', 'wb'))



    def trigrams_(self):

        for sentence in self.sentences:
            words = word_tokenize(sentence)
            for w1, w2, w3 in trigrams(words, pad_right=True, pad_left=True):
                if w1 == None:
                    w1 = '<s>'
                if w2 == None:
                    w2 = '<s>'
                if w3 == None:
                    w3 = '<s>'
                w1 = str(w1).lower()
                w2 = str(w2).lower()
                w3 = str(w3).lower()
                self.model[(w1, w2)][w3] += 1
                self.totals += 1


    def bigrams_(self):

        for sentence in self.sentences:
            words = word_tokenize(sentence)
            for w1, w2 in bigrams(words, pad_right=True, pad_left=True):
                if w1 == None:
                    w1 = '<s>'
                if w2 == None:
                    w2 = '<s>'
                w1 = str(w1).lower()
                w2 = str(w2).lower()
                # print(w1,w2)
                
                self.model_bigrams[w1][w2] += 1
                self.totals_bigrams += 1


    def unigrams_(self):

        for sentence in self.sentences:
            words = word_tokenize(sentence)
            for w1 in words:
                if w1 == None or w1 == ' ':
                    w1 = '<s>'
                    print(w1)
                self.model_unigrams[w1] +=1
                self.total_unigram +=1

    def convert_to_pct(self):

        score = 0
        self.model_unigrams = dict(self.model_unigrams)
        for key, value in self.model_bigrams.items():
            
            
            
            token2 = ''


            for key1, value1 in value.items():

                if value1 > 0:
                    
                    score += math.log(value1)
                    # print(len)
                    score -= math.log(len(self.sentences))
                else:
                    score += math.log(0.4) + math.log(self.model_unigrams[key1]+1)
                    score -= math.log(self.total_unigram + len(self.model_unigrams))
                print(score)

                
                self.model_bigrams[(value1,key1)]

                if value1 > 0:
                    
                    score += math.log(value1)
                    # print(len)
                    score -= math.log(len(self.sentences))
                else:
                    score += math.log(0.4) + math.log(self.model_unigrams[value1]+1)
                    score -= math.log(self.total_unigram + len(self.model_unigrams))
                print(score)
                # else:
                #     score += math.log(0.4) + math.log(self.model_unigrams[token2]+1)
                #     score -= math.log(self.total + len(self.model_unigrams))
                # value[key1] = (value1 / self.totals_bigrams)
                # if value1 > 0:
                #     score2 += math.log(value1)
                #     score2 -= math.log(self.totals_bigrams + len(self.model_bigrams))
                #     value[key1] = score2
                # else:
                #     score2 -= math.log(self.totals_bigrams + len(self.model_bigrams))
                #     value[key1] = score2

                # mydict[valu1][key1]

        # {the: {a : 3 , job: 4,}
        # {
        #('the','a')   : 3,
        #('the','job') :4
        # }
        


        # for key, value in self.model_bigrams.items():
        #     self.model_bigrams[key] = dict(sorted(value.items(), key=lambda x: x[1], reverse=True))

        

        # # Divide with total counts
        # self.model_unigrams = dict(self.model_unigrams)
        # score3 = 0
        # for key, value in self.model_unigrams.items():
        #     # self.model_unigrams[str(key)] = (value / self.total_unigram)
        #     if value > 0:
        #             score3 += math.log(value)
        #             score3 -= math.log(self.total_unigram + len(self.model_unigrams))
        #             self.model_unigrams[key] = score3
        #             # print(self.model_unigrams[key])
        #     else:
        #         score3 -= math.log(self.total_unigram + len(self.model_unigrams))
        #         self.model_unigrams[key] = score3


        # # Sort Dictionary
        
        # self.model_unigrams = dict(sorted(self.model_unigrams.items(), key=lambda x: x[1], reverse=True))
        


if __name__ == '__main__':
    import setup
    # Stand alone test
    # first_exe()

    # In the first usage uncomment the following function to train the model
    model_train()
