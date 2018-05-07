# -*- coding: utf-8 -*-　　
# -*- coding: cp950 -*-
from os import walk
import csv
import json
import sys

reload(sys)
sys.setdefaultencoding("utf8")

filename = "feedback.csv"

article_id = []
article_content = []
feedback_id = []
feedback_content = []
feedback_created_time = []


def readcsv(filename):
    with open(filename, 'rb') as file:
        reader = csv.reader(file)
        reader.next()
        for row in reader:
            feedback_id.append(row[0])
            article_id.append(row[1])
            article_content.append(row[2])
            feedback_content.append(row[3])
            feedback_created_time.append(row[4])


def printcsv(article_id, feedback_content):
    filename = "data/article" + str(article_id) + "_feedback.csv"
    with open(filename, "wb") as file:
        writer = csv.writer(file)
        data = json.loads(feedback_content)
        writer.writerow(["index_start",
                         "index_end",
                         "mod_history",
                         "mod_type",
                         "modifier",
                         "mod_comment"])
        for item in data:
            writer.writerow([item["index_start"],
                             item["index_end"],
                             item["mod_history"],
                             item["mod_type"],
                             item["modifier"],
                             item["mod_comment"].encode("utf-8")])


def printtxt(article_id, txt_content):
    filename = "data/article" + str(article_id) + ".txt"
    with open(filename, "wb") as file:
        content = txt_content.lstrip()
        file.write(content)


def print_doc():
    data_count = len(article_id)
    for i in range(data_count):
        printcsv(article_id[i], feedback_content[i])
        printtxt(article_id[i], article_content[i])


readcsv(filename)
print_doc()
