# Auto Classifying Tool

## Enviroments
* Python 2.7.3
* Python packages
	* nltk
	* Pattern
	* python-rake 

## Execution and Arguments
`$ python readdb.py`

* Read and extract feedbacks and articles from feedback pulled from csv
* Generate `article[article_number].txt` and `article[article_number]_feedback.csv`

`$ python classify.py [article_number]`

* Read text file and feedback csv file of article i and write new classification to new files named `article[i]_feedback_mod.csv`

## Preprocessing
`def read_feedback`

* Seperate original feedback into text before modification and text after modification

`def modify`

* Replacing special characters, ex: `"’"` to `"'"`, `"“"` to `"""`
* Replacing tab to one space (need improvment)
* Seperate original feedback into text before modification and text after modification
* Completing words:
	* add characters appear after the word to the rear until meeting a space or punctuation
	* add characters appear before the word to the head until meeting a space or punctuation

## Comments' Sentiment Analyzing


## Mechanical Mistakes


## Grammar Mistakes
## Vocabulary Mistakes