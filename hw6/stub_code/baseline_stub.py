#!/usr/bin/env python
'''
Created on May 14, 2014
@author: reid

Modified on May 21, 2015
'''

import sys
import nltk
import operator

# Read the file from disk


def read_file(filename):
    fh = open(filename, 'r')
    text = fh.read()
    fh.close()

    return text

# The standard NLTK pipeline for POS tagging a document


def get_sentences(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    return sentences


def get_bow(tagged_tokens, stopwords):
    return set([t[0].lower() for t in tagged_tokens if t[0].lower() not in stopwords])


def find_phrase(tagged_tokens, qbow):
    for i in range(len(tagged_tokens) - 1, 0, -1):
        word = (tagged_tokens[i])[0]
        if word in qbow:
            return tagged_tokens[i + 1:]


# qtokens: is a list of pos tagged question tokens with SW removed
# sentences: is a list of pos tagged story sentences
# stopwords is a set of stopwords

# Removes duplicate words
def removeDuplicates(answerList):
    final = []
    for a in answerList:
        if a not in final:
            final.append(a)
    return final


# if it is a who question, then we only want nouns
def getOnlyNouns(answerList):
    onlyNouns = []
    acceptable = ['NN', 'NNS', 'NNP', 'DT', 'JJ']
    for a in answerList:
        if a[1] in acceptable:
            onlyNouns.append(a[0])
    return onlyNouns


# Remove all words in question from answer
def removeQuestionWords(question, answer):
    removed_list = []
    questionWords = nltk.word_tokenize(question)
    # all answers are in lowercase
    # so let's do the same with the question text
    questionWords = [w.lower() for w in questionWords]
    Wlist = ['who', 'what', 'where']
    for a in answer:
        word = a[0]
        if word.lower() not in questionWords:
            removed_list.append(word)
    if 'who' in questionWords:
        removed_list = getOnlyNouns(answer)
    removed_list = removeDuplicates(removed_list)
    return removed_list


def baseline(qbow, sentences, stopwords):
    # Collect all the candidate answers
    answers = []
    for sent in sentences:
        # A list of all the word tokens in the sentence
        sbow = get_bow(sent, stopwords)

        # Count the # of overlapping words between the Q and the A
        # & is the set intersection operator
        overlap = len(qbow & sbow)

        answers.append((overlap, sent))

    # Sort the results by the first element of the tuple (i.e., the count)
    # Sort answers from smallest to largest by default, so reverse it
    answers = sorted(answers, key=operator.itemgetter(0), reverse=True)

    # Return the best answer
    best_answer = (answers[0])[1]
    return best_answer

if __name__ == '__main__':
    text_file = "fables-01.sch"

    stopwords = set(nltk.corpus.stopwords.words("english"))
    text = read_file(text_file)
    question = "Where was the crow sitting?"
    # qbow contains the bag of words for the answer
    qbow = get_bow(get_sentences(question)[0], stopwords)
    sentences = get_sentences(text)
    # baseline finds the most overlapped sequence from qbow
    answer = baseline(qbow, sentences, stopwords)

    print(" ".join(t[0] for t in answer))
