import constituency_demo_stub
import read_write_stub
from nltk.tree import Tree
import nltk
import sys


def read_file(file_name):
    # getting the correct story files
    story_ids = []
    f = open(file_name, 'r')
    lines = f.readlines()
    for line in lines:
        story_ids.append(line.rstrip('\n'))
    f.close()
    return story_ids


def process_command(story_list):
    # IN: story_id.txt from command line
    # OUT:
    for fname in story_list:
        # print(fname)
        data_dict = read_write_stub.get_data_dict(fname)
        questions = read_write_stub.getQA("{}.questions".format(fname))
        # print(len(questions))
        for q in range(0, len(questions)):
            qname = "{0}-{1}".format(fname, q + 1)
            qtypes = questions[qname]['Type']
            # print(qtypes)
            # qtypes can be "Story", "Sch", "Sch | Story"
            for qt in qtypes.split("|"):
                qt = qt.strip().lower()
                # These are the text data where you can look for answers.
                raw_text = data_dict[qt]
                par_text = data_dict[qt + ".par"]

                sentences = []
                for line in par_text.split('\n'):
                    sentences.append(line)
                # print(sentences)
                # print(par_text)
                # trees = [Tree.fromstring(line) for line in sentences]
                parse_filename = fname + "." + qt + ".par"
                trees = constituency_demo_stub.read_con_parses(parse_filename)

                qpar_fname = fname + ".questions.par"
                question_trees = constituency_demo_stub.process_question_file(
                    qpar_fname)
                print(question_trees)
        print()  # new line per question


if __name__ == '__main__':
    input_file_name = sys.argv[1]
    story_list = read_file(input_file_name)
    process_command(story_list)
