import os


###### Create Directories  #######
##################################


### MODELS
path = os.getcwd()
try:
	os.mkdir(path+'/models')
except FileExistsError:
	pass