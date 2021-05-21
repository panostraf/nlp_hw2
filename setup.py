### HW_2 ### 
### NLP  ###
### Trafalis Panagiotis ###
### Ioannis Fitsopoulos ###
### Eirini Nomikou ###


import os


###### Create Directories  #######
##################################


### MODELS
path = os.getcwd()
try:
	os.mkdir(path+'/models')
except FileExistsError:
	pass



def setup():
    import nltk
    nltk.download('words')
    nltk.download('punkt')

