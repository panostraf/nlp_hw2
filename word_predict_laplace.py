### HW_2 ### 
### NLP  ###
### Trafalis Panagiotis ###
### Ioannis Fitsopoulos ###
### Eirini Nomikou ###



from nltk import bigrams,trigrams
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
import pickle

class PredWord:

    def __init__(self):
        self.model = dict(pickle.load(open('models/trigram_model_laplace.p', 'rb')))
        self.model_bigram = dict(pickle.load(open('models/bigram_model_laplace.p','rb')))
        self.model_unigram = dict(pickle.load(open('models/unigram_model_laplace.p','rb')))

    def predict_word(self, text):

        words = word_tokenize(text)
        if len(words) < 2:
            try:
                w0 = words[-1]
                pred_w  = list(self.model_bigram[w0])[0]
                # print(pred_w)
                return pred_w
                
            except KeyError:
                try:
                    w0 = words[-1]
                    pred_w = list(self.model_unigram[str(w0)])[0]
                    ### TODO UNIGRAM
                    # print(pred_w)
                    return pred_w
                except:
                    # print('no prediction')
                    return None
                    
        else:
            try:
                w0 = words[-2]
                w1 = words[-1]
                pred_w = list(self.model[(w0, w1)].keys())[0]
                # print(pred_w)
                return pred_w

            except KeyError:

                try:
                    w0 = None
                    w1 = words[-1]
                    pred_w = list(self.model[(w0, w1)].keys())[0]
                    # print(pred_w)
                    return pred_w

                except KeyError:
                    try:
                        w0 = words[-1]
                        pred_w  = list(self.model_bigram[w0])[0]
                        # print(pred_w)
                        return pred_w

                    except KeyError:
                        try:
                            w0 = words[-1]
                            pred_w = list(self.model_unigram[str(w0)])[0]
                            # print(pred_w)
                            return pred_w
                        except:
                            return None


# if __name__ == '__main__':
#     # Stand Alone Test
#     lang_mod = PredWord()

#     # user input to predict the next word
#     while True:
#         test = input('Type here:\n').lower()
#         if test == 'exit_now':
#             break
#         lang_mod.predict_word(test)


