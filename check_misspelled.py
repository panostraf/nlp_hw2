import math
import pickle
import collections
from nltk import sent_tokenize, word_tokenize


class LaPlaceModel:

  def __init__(self,model):
      self.model = model
      self.score = 0
      self.totals = 0
      self.len = len(self.model)

  def score_trigram(self):
      self.totals = self.sum_all()
      for key, value in self.model.items():
          for key1, value1 in value.items():
              if value1 > 0:
                  self.score += -math.log(value1+1)
                  self.score -= -math.log(self.totals + self.len)      
              else:
                  self.score -= -math.log(self.totals + self.len)

  def score_bigram(self):
      self.totals = self.sum_all()
      for key, value in self.model.items():
          for key1, value1 in value.items():
              if value1 > 0:
                  self.score += -math.log(value1+1)
                  self.score -= -math.log(self.totals + self.len)      
              else:
                  self.score -= -math.log(self.totals + self.len)

  def score_unigram(self):
      for key, value in self.model.items():
          if value > 0:
                  self.score += -math.log(value+1)
                  self.score -= -math.log(self.totals + len(self.model))
          else:
              self.score -= -math.log((self.totals) + len(self.model))

  def sum_all(self):
      total = 0
      for key, value in self.model.items():
          total += sum(value.values())
      return total

class StupidBackOff:
  def __init__(self,trigram,bigram,unigram):
      self.trigram = trigram
      self.bigram = bigram
      self.unigram = unigram

      self.trigram_totals = self.sum_all(trigram)
      self.bigram_totals = self.sum_all(bigram)
      self.unigram_totals = sum(unigram.values())


      self.score = self.trigram_score()
      self.score2 = self.bigram_score()

  def sum_all(self,model):
      total = 0
      for key, value in model.items():
          total += sum(value.values())
      return total


  def trigram_score(self):
      score = 0
      for key,value in self.trigram.items():
          for key1,value1 in value.items():
              # print(key1)
              count = self.trigram[key][key1]
              # print(count)
              if count > 0:
                  try:
                      score += -math.log(count)
                      score -= -math.log(self.bigram[key[1]][key1]+1)
                  except:
                      score += -math.log(count)
                      score -= -math.log(1)

              else:
                  try:
                      score += -math.log(0.4) + math.log(self.bigram[key[1]] + 1)
                      score -= -math.log(self.bigram + len(self.bigram.keys()))
                  except KeyError:
                      score += -math.log(0.4) + math.log(1)
                      score -= -math.log(self.bigram + len(self.bigram.keys()))
      return round(score)

  def bigram_score(self):
      score = 0
      for key,value in self.bigram.items():
          for key1,value1 in value.items():
              # print(key1)
              count = self.bigram[key][key1]
              # print(count)
              if count > 0:
                  try:
                      score += -math.log(count)
                      score -= -math.log(self.unigram[key1]+1)
                  except KeyError:
                      score += -math.log(count)
                      score -= -math.log(1)

              else:
                  try:
                      score += -math.log(0.4)*(0.4) + math.log(self.unigram[key1] + 1)
                      score -= -math.log(self.unigram + len(self.unigram.keys()))
                  except:
                      score += -math.log(0.4)*(0.4) + math.log(1)
                      score -= -math.log(self.unigram + len(self.unigram.keys()))
      return round(score)


def main_LP():
  # Read Saved Models
  unigram = dict(pickle.load(open('models/unigram_model.p', 'rb')))
  bigram = dict(pickle.load(open('models/bigram_model.p', 'rb')))
  trigram = dict(pickle.load(open('models/trigram_model.p', 'rb')))
  # Creade object for each model
  unigram_laplace = LaPlaceModel(model = unigram)
  bigram_laplace = LaPlaceModel(model = bigram)
  trigram_laplace= LaPlaceModel(model = trigram)

  # Calculate score for each model
  bigram_laplace.score_bigram()
  trigram_laplace.score_trigram()
  sbo = StupidBackOff(trigram,bigram,unigram)

  # Print Results
  print('bigram_laplace',round(bigram_laplace.score/1000))    
  print('bigram_SBO',round(sbo.score2/1000))


  print('trigram_laplace',round(trigram_laplace.score/1000))
  print('trigram_SBO',round(sbo.score/1000))


if __name__ == '__main__':
  main_LP()
