### HW_2 ### 
### NLP  ###
### Trafalis Panagiotis ###
### Ioannis Fitsopoulos ###
### Eirini Nomikou ###

import word_predict_laplace
import word_predict
from nltk.tokenize import sent_tokenize, word_tokenize
from random import sample

class CompareModels:
	def __init__(self,testfile):
		self.text = open(testfile, 'r').read()
		self.sentences = sample([sentence for sentence in sent_tokenize(self.text)],1000)
		self.lang_model_laplace = word_predict_laplace.PredWord()
		self.lang_model = word_predict.PredWord()
		self.lp_score = 0
		self.basic_score = 0
		self.all_ = 0


	def compare(self):

		for sentence in self.sentences:
			# print(sentence)
			words = [word for word in word_tokenize(sentence)]

			for i in range(len(words)):
				if len(words[:-i]) > 0:

					sent = ' '.join(words[:-i]) if len(words[:-i]) > 0 else ''
					# print('sentence = ',sent)
					correct_word = words[-i]
					# print('correct word =',correct_word)
								
					w1 = self.lang_model.predict_word(sent)
					w2 = self.lang_model_laplace.predict_word(sent)
					# print('w1',w1)
					# print('w2',w2)
					if w1 == correct_word:
						self.basic_score +=1
					if w2 == correct_word:
						self.lp_score +=1
					self.all_ +=1
				else:
					continue

if __name__ == '__main__':
	### TEST STAND ALONE ###
	comp = CompareModels('big.txt')
	comp.compare()


	print('No Smothing: ' , round((comp.basic_score / comp.all_)*100,2),"%")
	print('LaPlace Smothing' , round((comp.lp_score / comp.all_)*100,2),"%")
	
	print('Tested with',comp.all_,'sentences')