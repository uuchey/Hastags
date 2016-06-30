# -*- coding: utf-8 -*-

import glob
from itertools import groupby
import re

punctuation = ".,:;!?'"   # creating the string out of punctuation characters
stop_words = [word.strip().lower() for word in open('StopWords.csv')]


def getFilesInDir():

    filenames = glob.glob('./*.txt')
    for i in range(len(filenames)):
        filenames[i] = filenames[i][2:]
    return filenames


def textToWords(text):

    words = []

    for line in text.split('\n'):

        output = ""
        prev = ""   # keeping track of previous letter

        for char in line:
            if char.isalpha():             # if character is a letter add it to output and assign it to prev
                output += char.lower()
                prev = char.lower()
            elif char == " " or char in punctuation:    # if character is a blank space or a punctuation add blank space only if previous character is a letter (not to have unnecessary blanks)
                if prev.isalpha():
                    output += " "
                    prev = " "

        output_list = output.split(" ")  # split text into list of words
        output_list = [word for word in output_list if (word not in stop_words and len(word) > 2)]

        words.extend(output_list)
    return words


files = getFilesInDir()
words_in_files = {}
len_words = {}
words_in_sentences = {}

for file in files:

    file_name = file[:-4]

    text = open(file).read()

    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

    for sentence in sentences:
        processed_sentence = textToWords(sentence)

        for word in processed_sentence:
            if word not in words_in_files:
                words_in_files[word] = [file_name]
            else:
                words_in_files[word].append(file_name)
            if word not in words_in_sentences:
                words_in_sentences[word] = [sentence]
            else:
                words_in_sentences[word].append(sentence)

    for word in words_in_files:
        len_words[word] = len(words_in_files[word])

max_words = sorted(len_words, key=len_words.get, reverse=True)[:10]

for w in max_words:

    wif = [ key for key,_ in groupby(words_in_files[w])]
    print ("Word:", w)
    print ("In documents:", ', '.join(list(wif)))
    print ("In sentences:")
    line = 0
    for sntnc in set(words_in_sentences[w]):

        print (line, sntnc.strip())
        line += 1
    print










