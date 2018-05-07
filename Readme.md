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
`def pos_neg`

* Determine whether the comment is positive or negative
* If any of positive or negative is larger than 0, then compare them and output the larger one, otherwise output "Neural"

`def extract_keywords`

* Using RAKE(Rapid Automatic Keyword Extraction) algorithm to extract keywords of comments

## Mechanical Mistakes
`def mechanical`

* Detecting capitalize problems: see if the lowercase of original text and the lowercase of modified text are the same
* Detecting punctuation problems: see if only punctuation are modified

## Grammar Mistakes
`def grammar`

* Detecting errors of definite article, ex: "the" to "a".
* Detecting errors of tenses by determining if the stem and the conjugation of the original text and modified text are the same.
	* NLTK stem function
	* pattern.en conjugate function

## Vocabulary Mistakes
* Modifications other than Mechanical Errors and Grammar Errors