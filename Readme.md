# Auto Classifying Tool

## Enviroments
* Python 2.7.3
* Python packages
	* nltk
	* Pattern
	* python-rake 

## Execution and Arguments
1. Read and extract feedbacks and articles from feedback pulled from csv
`$ python readdb.py`
 - generate `article[article_number].txt` and `article[article_number]_feedback.csv`
2. Read text file and feedback csv file of article i and write new classification to new files named `article[i]_feedback_mod.csv`
`$ python classify.py [article_number]`

## Comments' Sentiment Analyzing

## Mechanical Mistakes
## Grammar Mistakes
## Vocabulary Mistakes