import zipfile
import os
import re
import nltk
from collections import OrderedDict
# from read_write_stub import getQA
# from baseline_stub import get_bow
# from baseline_stub import baseline
import baseline_stub
import read_write_stub

if __name__ == '__main__':
    stopwords = set(nltk.corpus.stopwords.words("english"))
    cname_size_dict = OrderedDict()
    cname_size_dict.update({"fables": 2})
    cname_size_dict.update({"blogs": 1})
    for cname, size in cname_size_dict.items():
        for i in range(0, size):
            # File format as fables-01, fables-11
            fname = "{0}-{1:02d}".format(cname, i + 1)
            #print("File Name: " + fname)
            data_dict = read_write_stub.get_data_dict(fname)

            questions = read_write_stub.getQA("{}.questions".format(fname))
            for j in range(0, len(questions)):
                qname = "{0}-{1}".format(fname, j + 1)
                if qname in questions:
                    #print("QuestionID: " + qname)

                    question = questions[qname]['Question']
                    print(question)

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
                    print(" ".join(t[0] for t in answer))
                    # print(answer)
