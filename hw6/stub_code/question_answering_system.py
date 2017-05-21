import zipfile
import os
import re
import nltk
from nltk import Tree
from collections import OrderedDict
# from read_write_stub import getQA
# from baseline_stub import get_bow
# from baseline_stub import baseline
import baseline_stub
import read_write_stub


def file_write(file_name, text_list):
    f = open(file_name, 'w')
    for line in text_list:
        f.write(line + "\n")
    f.close()


# def read_con_parse(parse_file):
#     fh = open(parse_file, 'r')
#     lines = fh.readlines()
#     fh.close()
#     return [nltk.Tree.parse(line) for line in lines]


def filterResponse(answer_pos_tag):
    # IN, DT, NN, IN, DT NN,
    # DT, NN, IN, NN
    # DT, NNP, CC, DT, NNP
    # DT, NN
    # DT, JJ, NNP
    # DT, NNP
    # IN, DT, NN, RB, VBD
    # TO, VB, DT, NN
    # IN, DT, NN, FBD, JJ, DT, NN, IN, DT, NN
    # IN, JJ, NN
    # NNP, NN
    # DT, NNS, VBD
    # VBD
    # DT, NNS
    # DT, NN, NN
    # VBD, VBN
    # JJ, NN, NNS
    # NNS, IN, NNS
    acceptable_list = ['IN', 'DT', 'NN', 'CC', 'NNP',
                       'JJ', 'RB', 'VBD', 'FBD', 'NNS', 'VBN', 'VB']
    filtered_response = []
    for a in answer_pos_tag:
        if a[1] in acceptable_list:
            filtered_response.append(a[0])
    return filtered_response


if __name__ == '__main__':
    output_file_name = 'train_my_answers.txt'
    output_text = []
    stopwords = set(nltk.corpus.stopwords.words("english"))
    cname_size_dict = OrderedDict()
    cname_size_dict.update({"fables": 2})
    cname_size_dict.update({"blogs": 1})
    for cname, size in cname_size_dict.items():
        for i in range(0, size):
            # File format as fables-01, fables-11
            fname = "{0}-{1:02d}".format(cname, i + 1)
            # question_par_filename = fname + ".questions.par"
            # question_parse_list = read_con_parse(question_par_filename)
            # # print(question_parse_list)
            # story_par_filename = fname + ".story.par"
            # story_parse_list = read_con_parse(story_par_filename)
            # print("File Name: " + fname)
            data_dict = read_write_stub.get_data_dict(fname)

            questions = read_write_stub.getQA("{}.questions".format(fname))
            for j in range(0, len(questions)):
                qname = "{0}-{1}".format(fname, j + 1)
                if qname in questions:
                    # print("QuestionID: " + qname)

                    question = questions[qname]['Question']
                    question_postag = nltk.pos_tag(
                        nltk.word_tokenize(question))

                    question_line = "QuestionID: {}".format(qname)
                    # print(question_postag)
                    output_text.append(question_line)

                    # Getting the story filename
                    qtypes = questions[qname]['Type']
                    for qt in qtypes.split("|"):
                        qt = qt.strip().lower()
                        raw_text = data_dict[qt]

                    # # Getting text from the story filename
                    # text = baseline_stub.read_file(raw_text)

                    # Getting the bag of words
                    qbow = baseline_stub.get_bow(
                        baseline_stub.get_sentences(question)[0], stopwords)

                    # Gets sentences
                    sentences = baseline_stub.get_sentences(raw_text)
                    answer = baseline_stub.baseline(qbow, sentences, stopwords)
                    answer_default = " ".join(t[0] for t in answer)

                    # FILTERING
                    filtered_answer = filterResponse(answer)
                    filtered_text = " ".join(t for t in filtered_answer)

                    # REMOVE QUESTION WORDS
                    # removed_question_words = baseline_stub.removeQuestionWords(
                    #     question, answer)
                    # answer_text = " ".join(t for t in removed_question_words)

                    answer_prepend = "Answer: "

                    # COMPARE TO DEFAULT HERE
                    answer_total = answer_prepend + filtered_text  # FILTERED
                    # answer_total = answer_prepend + answer_default # DEFAULT
                    output_text.append(answer_total + '\n')
    file_write(output_file_name, output_text)
