# Installation
  git init
  git git clone https://github.com/panostraf/nlp_hw2.git

# Create venv
  mkdir venv
  python -m venv venv

# Activate virtual enviroment
  source venv/Scripts/activate (for windows)
  source venv/bin/activate (for mac or linux)

# Install requirements
  pip install --upgrade pip (or pip3 install --upgrade pip)
  pip install -r requirements.txt

-----------------------------------------------------------------

Files:

  setup.py -- Creates necessary directories and downloads NLTK's packages
  score.py -- evaluates different models and prints the according score in the terminal
  
  train_model.py -- builts trigram - bigram - unigram models and saves them in model directory
  		   In pickle format
  
  word_predict.py -- starts a loop in the terminal where asks to type a sentence, and will
		    will attempted to predict the next word

  check_misspelled.py -- Tries to correct all the words in the provided sentence based on 
                         Minimum edit distance and the language model
  

