#!/usr/bin/env python
'''
Created on May 14, 2014
@author: reid

Modified on May 21, 2015
'''

import sys
import nltk
import operator
from nltk.stem.lancaster import LancasterStemmer
import re
import pprint
import csv
from collections import defaultdict
from nltk.corpus import wordnet as wn
import wordnet_demo

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


def get_stems(word_list):
    st = LancasterStemmer()
    stem_list = []
    for w in word_list:
        stem_list.append(st.stem(w))
    return set(stem_list)


def get_wordnet(word):
    wordnet_list = []
    noun_ids = wordnet_demo.load_wordnet_ids("Wordnet_nouns.csv")
    verb_ids = wordnet_demo.load_wordnet_ids("Wordnet_verbs.csv")

    # for synset_id, items in noun_ids.items():
    #     noun = items['story_noun']
    #     stories = items['stories']
    #     # print(noun, stories)
    #     # get lemmas, hyponyms, hypernyms

    # for synset_id, items in verb_ids.items():
    #     verb = items['story_verb']
    #     stories = items['stories']
    #     # print(verb, stories)
    #     # get lemmas, hyponyms, hypernyms

    word_synsets = wn.synsets(word)
    for synset in word_synsets:
        # GENERAL TO SPECIFIC
        hyponyms = synset.hyponyms()
        for hypo in hyponyms:
            wordnet_list.append(hypo.name()[0:hypo.name().index(".")])
        # SPECIFIC TO GENERAL
        hypernyms = synset.hypernyms()
        for hyper in hypernyms:
            wordnet_list.append(hyper.name()[0:hyper.name().index(".")])
    return set(wordnet_list)


def stem_baseline(qbow, sentences, stopwords):
    # returns list of top 3 answers using stemming
    answers = []
    for sent in sentences:
        sbow = get_bow(sent, stopwords)
        # Stemming Overlap
        q_stems = get_stems(qbow)  # stemming question bag of words
        s_stems = get_stems(sbow)  # stemming sentence bag of words
        stem_overlap = len(q_stems & s_stems)
        answers.append((stem_overlap, sent))
    answers = sorted(answers, key=operator.itemgetter(0), reverse=True)
    first_answer = (answers[0])[1]
    second_answer = (answers[0])[1]
    third_answer = (answers[0])[1]
    answer_list = [first_answer, second_answer, third_answer]
    return answer_list

# qtokens: is a list of pos tagged question tokens with SW removed
# sentences: is a list of pos tagged story sentences
# stopwords is a set of stopwords


def wordnet_baseline(qbow, sentences, stopwords):
    answers = []
    for sent in sentences:
        # A list of all the word tokens in the sentence
        sbow = get_bow(sent, stopwords)
        qwordnet = set()
        for word in qbow:
            temp_qwordnet = get_wordnet(word)
            qwordnet = qwordnet.union(temp_qwordnet)
        # print("QWORDNET: {}".format(qwordnet))
        wordnet_overlap = len(qwordnet & sbow)
        answers.append((wordnet_overlap, sent))
    answers = sorted(answers, key=operator.itemgetter(0), reverse=True)
    first_answer = (answers[0])[1]
    second_answer = (answers[1])[1]
    third_answer = (answers[2])[1]
    answer_list = [first_answer, second_answer, third_answer]
    return answer_list


def baseline(qbow, sentences, stopwords):
    # Collect all the candidate answers
    answers = []
    for sent in sentences:
        # A list of all the word tokens in the sentence
        sbow = get_bow(sent, stopwords)
        # Count the # of overlapping words between the Q and the A
        # & is the set intersection operator
        overlap = len(qbow & sbow)

        # OPTION: TOGGLE STEMMING HERE
        answers.append((overlap, sent))

    # Sort the results by the first element of the tuple (i.e., the count)
    # Sort answers from smallest to largest by default, so reverse it
    answers = sorted(answers, key=operator.itemgetter(0), reverse=True)

    # Return the best answer
    # best_answer = (answers[0])[1]
    # return best_answer
    first_answer = (answers[0])[1]
    second_answer = (answers[1])[1]
    third_answer = (answers[2])[1]
    answer_list = [first_answer, second_answer, third_answer]

if __name__ == '__main__':
    text_file = "fables-01.sch"

    stopwords = set(nltk.corpus.stopwords.words("english"))
    text = read_file(text_file)
    question = "Where was the crow sitting?"

    qbow = get_bow(get_sentences(question)[0], stopwords)
    print("qbow: {}".format(qbow))
    sentences = get_sentences(text)

    answer = baseline(qbow, sentences, stopwords)

    print(" ".join(t[0] for t in answer))
