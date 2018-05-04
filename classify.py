# -*- coding: utf-8 -*-　　
# -*- coding: cp950 -*-
import argparse
import csv
import nltk
import operator
import string
import sys
import RAKE
import re

from os import walk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from pattern.en import conjugate

nltk.downloader.download('vader_lexicon')
nltk.download('wordnet')

reload(sys)
sys.setdefaultencoding("utf8")

count = 0
index_start = []
index_end = []
mod_type = []
new_type = []
org_content = []
mod_content = []
mod_comment = []
mod_hist = []
modifier = []


def read_feedback(feedback_num):
    global count
    global index_start
    global index_end
    global mod_type
    global new_type
    global org_content
    global mod_content
    global mod_comment

    csv_filename = "data/article" + feedback_num + "_feedback.csv"

    with open(csv_filename, "rb") as file:
        reader = csv.reader(file)
        reader.next()
        for row in reader:
            index_start.append(row[0])
            index_end.append(row[1])
            mod_hist.append(row[2])
            mod_type.append(row[3])
            modifier.append(row[4])
            mod_comment.append(row[5])
            new_type.append("")
            if row[3] == "Insert":
                org_content.append("")
                mod_content.append(row[2][1:-1])
            elif row[3] == "Delete":
                org_content.append(row[2][1:-1])
                mod_content.append("")
            elif row[3] == "Replace":
                phrase = row[2].split(" with ")
                org_content.append(phrase[0][1:-1])
                mod_content.append(phrase[1][1:-1])
            else:
                org_content.append("")
                mod_content.append("")


def space_and_punctuation(input_string, start_or_end):
    if len(input_string) == 0:
        return False
    if start_or_end == "Start":
        if input_string[0] == " " or input_string[0] in string.punctuation:
            return True
    elif start_or_end == "End":
        if input_string[-1] == " " or input_string[-1] in string.punctuation:
            return True
    return False


def modify(feedback_num):
    global org_content
    global mod_content

    txt_filename = "data/article" + feedback_num + ".txt"

    count = len(index_start)
    with open(txt_filename, "rb") as file:
        text = file.read()
        content = re.sub("\s\s", "", text)
        content = content.replace("’", "'").replace("“", "\"").replace("”", "\"")
        # print content
        # print text

    # for i in range(449, 525):
    #     print i, content[i]
    for i in range(len(content)):
        print i, content[i]
    for i in range(count):
        if mod_type[i] == "Comment":
            continue
        # trailing
        if not space_and_punctuation(org_content[i], "End") and\
           not space_and_punctuation(mod_content[i], "End"):
            end = int(index_end[i])
            suffix = ""
            while end < len(index_end) and content[end] not in string.punctuation and content[end] != " ":
                suffix += content[end]
                end += 1
            org_content[i] += suffix
            mod_content[i] += suffix
        # leading
        if not space_and_punctuation(org_content[i], "Start") and\
           not space_and_punctuation(mod_content[i], "Start"):
            start = int(index_start[i]) - 2
            prefix = ""
            while content[start] not in string.punctuation and content[start] != " ":
                prefix = content[start] + prefix
                start -= 1
            org_content[i] = prefix + org_content[i]
            mod_content[i] = prefix + mod_content[i]


def mechanical(original, modify):
    # typo
    original = original.strip()
    modify = modify.strip()
    if original.lower() == modify.lower():
        return True

    # punctuation
    if len(original) > 1 or len(modify) > 1:
        return False
    if len(original) == 1 and original[0] in string.punctuation or \
       len(modify) == 1 and modify[0] in string.punctuation:
        return True
    return False


def grammar(original, modify):
    original_list = original.translate(None, string.punctuation).split()
    modify_list = modify.translate(None, string.punctuation).split()
    wnl = WordNetLemmatizer()
    ps = PorterStemmer()

    # print original_list
    # print modify_list

    if len(original_list) <= 1 and len(modify_list) <= 1:
        if len(original_list) == 1:
            ori = original_list[0].strip().lower()
        else:
            ori = ""
        if len(modify_list) == 1:
            mod = modify_list[0].strip().lower()
        else:
            mod = ""
        # print ori
        # print mod
        if ori == "" or ori == "the" or ori == "a" or ori == "an":
            if mod == "" or mod == "the" or mod == "a" or mod == "an":
                return True

    for i in range(len(original_list)):
        print original_list[i]
        original_list[i].strip()
        original_list[i] = ps.stem(original_list[i])
        original_list[i] = conjugate(original_list[i], "inf")
    for i in range(len(modify_list)):
        print modify_list[i]
        modify_list[i].strip()
        modify_list[i] = ps.stem(modify_list[i])
        modify_list[i] = conjugate(modify_list[i], "inf")

    # print original_list
    # print modify_list

    if original_list == modify_list:
        # print True
        # print "======================="
        return True
    # print "======================="


def pos_neg(comment):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(comment)
    if ss["neu"] == 1:
        return "Neutral"
    else:
        if ss["neg"] > ss["pos"]:
            return "Negative"
        else:
            return "Positive"


def extract_keywords(comment):
    Rake = RAKE.Rake(RAKE.SmartStopList())
    result = Rake.run(comment, maxWords=3)
    keywords = []
    for item in result:
        keywords.append(item[0])

    return "Tags: " + ", ".join(keywords)


def nlpComment(comment):
    pos = pos_neg(comment)
    ext = extract_keywords(comment)
    return pos + ", " + ext


def classify():
    global org_content
    global mod_content

    count = len(index_start)
    for i in range(count):
        if mod_type[i] == "Comment":
            new_type[i] = nlpComment(mod_comment[i])
        else:
            if mechanical(org_content[i], mod_content[i]) is True:
                new_type[i] = "Mechanical"
            elif grammar(org_content[i], mod_content[i]) is True:
                new_type[i] = "Grammar"
            else:
                new_type[i] = "Vocabulary"


def printcsv(feedback_num):
    filename = "data/article" + feedback_num + "_feedback_mod.csv"
    count = len(index_start)
    with open(filename, "wb") as file:
        writer = csv.writer(file)
        writer.writerow(["index_start",
                         "index_end",
                         "mod_type",
                         "modifier",
                         "new_type",
                         "mod_history",
                         "org_content",
                         "mod_content",
                         "mod_comment"])
        for i in range(count):
            writer.writerow([index_start[i],
                             index_end[i],
                             mod_type[i],
                             modifier[i],
                             new_type[i],
                             mod_hist[i],
                             org_content[i],
                             mod_content[i],
                             mod_comment[i]])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("num", type=str)
    args = parser.parse_args()
    feedback_num = args.num
    read_feedback(feedback_num)
    modify(feedback_num)
    classify()
    printcsv(feedback_num)
