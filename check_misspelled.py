import re
import string
from collections import Counter
import numpy as np
from nltk.corpus import words
import pickle
import word_predict_laplace
import collections
from collections import defaultdict
from nltk.tokenize import word_tokenize


class SpellChecker(object):

  def __init__(self, corpus_file_path):
    # with open(corpus_file_path, "r") as file:
    #   lines = file.readlines()
    #   words = []
    #   for line in lines:
    #     words += re.findall(r'\w+', line.lower())

    self.vocabs = set(words.words())
    self.word_probas = dict(pickle.load(open('models/unigram_model_laplace.p','rb')))
    # self.vocabs = set(words) # words.words()
    # self.word_counts = Counter(words) #!
    # total_words = float(sum(self.word_counts.values()))#!
    # self.word_probas = {word: self.word_counts[word] / total_words for word in self.vocabs}#!
    # word_probas (lang model)


  def _level_one_edits(self, word):
    letters = string.ascii_lowercase
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [l + r[1:] for l,r in splits if r]
    swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r)>1]
    replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
    inserts = [l + c + r for l, r in splits for c in letters] 

    return set(deletes + swaps + replaces + inserts)

  def _level_two_edits(self, word):
    return set(e2 for e1 in self._level_one_edits(word) for e2 in self._level_one_edits(e1))

  def check(self, word):
    candidates = self._level_one_edits(word) or self._level_two_edits(word) or [word]
    valid_candidates = [w for w in candidates if w in self.vocabs]
    return sorted([(c, self.word_probas[c]) for c in valid_candidates], key=lambda tup: tup[1], reverse=True)



def split(word):
  return [(word[:i], word[i:]) for i in range(len(word) + 1)]


def delete(word):
  return [l + r[1:] for l,r in split(word) if r]


def swap(word):
  return [l + r[1] + r[0] + r[2:] for l, r in split(word) if len(r)>1]


def replace(word):
  letters = string.ascii_lowercase
  return [l + c + r[1:] for l, r in split(word) if r for c in letters]


def insert(word):
  letters = string.ascii_lowercase
  return [l + c + r for l, r in split(word) for c in letters]


def edit1(word):
  return set(delete(word) + swap(word) + replace(word) + insert(word))


def edit2(word):
  return set(e2 for e1 in edit1(word) for e2 in edit1(e1))


def correct_spelling(word, vocabulary, word_probabilities):
  if word in vocabulary:
    print(f"{word} is already correctly spelt")
    return 

def level_one(word):
  return set((delete(word)) + (swap(word))+ (insert(word)) + (replace(word)))
  
def level_two(word):
  return set(e2 for e1 in level_one(word) for e2 in level_one(e1))
  # return [word for word in candidates if word in vocabulary]


def spell_check(word,sentence):
  if word in vocabulary:
    # print('found it')
    return word

  else:
    sentence = sentence.rsplit(' ', 1)[0]
    

    sug1 = level_two(word).intersection(vocabulary)
    sug2 = level_one(word).intersection(vocabulary)
    suggestions = sug1.union(sug2)
    # print(suggestions)


    
    predict = word_predict_laplace.PredWord()

    words = [w for w in suggestions if w in vocabulary]
    # print("words in vocab:",words)

    # print('language model : ',predict.predict_word(sentence))

    model_unigram = dict(pickle.load(open('models/unigram_model_laplace.p','rb')))
    
    suggestions_dict = defaultdict(lambda:0)
    for w in words:

        try:

            suggestions_dict[w] = model_unigram[w]
        except KeyError:
            pass
    sorted_dict = collections.OrderedDict(suggestions_dict)
    

    try:
        if predict.predict_word(sentence) in suggestions_dict[w].keys():
            # print(predict.predict_word(sentence))
            return predict.predict_word(sentence)
    except:
        # print(list(sorted_dict)[0])
        try:
          return list(sorted_dict)[0]
        except IndexError:
          return word
    



if __name__ == '__main__':
  sentence = 'Homerk 1 and assocated iles has been posted inb tthe Crse Resourceees Folder/Homework Assig'
  while True:
    sentence = input()
    print(sentence)
    word = sentence.split()[-1]
    # print('word',word)
    vocabulary = words.words()

    corect_sentence = ''
    word_list = word_tokenize(sentence)
    for w in word_list:
      corect_sentence = f'{corect_sentence} {str(spell_check(w,sentence))}'
    print(corect_sentence)
    print('\n\n')

