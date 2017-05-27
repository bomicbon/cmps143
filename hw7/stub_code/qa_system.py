import constituency_demo_stub
import read_write_stub
from nltk.tree import Tree
import nltk
import baseline_stub
from baseline_stub import get_sentences
from baseline_stub import get_bow
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
    orig_stdout = sys.stdout
    out_filename = "data_results.txt"
    f = open(out_filename, 'w')
    sys.stdout = f
    stopwords = set(nltk.corpus.stopwords.words("english"))
    for fname in story_list:
        # print(fname)
        data_dict = read_write_stub.get_data_dict(fname)
        questions = read_write_stub.getQA("{}.questions".format(fname))
        # print(questions)
        # print(len(questions))
        for q in range(0, len(questions)):
            # QUESTION ID
            qname = "{0}-{1}".format(fname, q + 1)
            print("QuestionID: " + qname)
            # QUESTION TYPE
            qtypes = questions[qname]['Type']
            print("QuestionType: " + qtypes)
            # QUESTION STRING
            question = questions[qname]['Question']
            print("Question String: " + question)
            # QUESTION PAR
            # This list will hold all the questions in par tree format
            question_par_dict = {}  # qid : parse_tree
            # This is the .par stored as a string
            question_par_raw = data_dict["questions.par"]
            # print("Question Parse Tree: " + question_par + "\n")

            # Recreates the edited list
            parse_raw_list = question_par_raw.split("\n")
            for line in parse_raw_list:
                if not line:
                    pass
                else:  # line is not empty string
                    if line[0] == 'Q':
                        parse_ID = line[12:]  # cut from 'QuestionID: '
                        # print(parse_ID)
                    if line[0] == '(':
                        parse_line = line
                        question_par_dict[parse_ID] = parse_line
            # Look for matching QuestionIDs from the .par
            for key, value in question_par_dict.items():
                if qname == key:
                    # print(value + "\n")
                    question_parse_tree = constituency_demo_stub.make_tree(
                        value)
                    print(question_parse_tree)

            # ANSWER SEARCHING
            # qtypes can be "Story", "Sch", "Sch | Story"
            for qt in qtypes.split("|"):
                qt = qt.strip().lower()
                # These are the text data where you can look for answers.
                raw_text = data_dict[qt]
                par_text = data_dict[qt + ".par"]
                # SEND LINES TO A LIST
                raw_text_list = get_sentences(raw_text)
                par_text_list = par_text.split("\n")
                # REMOVE EMPTY FROM LIST
                par_text_list = filter(None, par_text_list)
                if qt == "story":
                    story_par_list = []  # initialize based on type
                    for r, p in zip(raw_text_list, par_text_list):
                        story_par_list.append((r, p))
                    qbow = get_bow(get_sentences(question)[0], stopwords)
                    answer = baseline_stub.baseline(
                        qbow, raw_text_list, stopwords)
                    answer_string = " ".join(t[0] for t in answer)
                    print("ANSWER: {}".format(answer_string))
                    for tuple in story_par_list:
                        if tuple[0] == answer:
                            answer_tree = constituency_demo_stub.make_tree(tuple[
                                                                           1])
                            print(answer_tree)

                if qt == "sch":
                    sch_par_list = []  # initialize based on type
                    for r, p in zip(raw_text_list, par_text_list):
                        sch_par_list.append((r, p))
                    qbow = get_bow(get_sentences(question)[0], stopwords)
                    answer = baseline_stub.baseline(
                        qbow, raw_text_list, stopwords)
                    answer_string = " ".join(t[0] for t in answer)
                    print("ANSWER: {}".format(answer_string))
                    for tuple in sch_par_list:
                        if tuple[0] == answer:
                            answer_tree = constituency_demo_stub.make_tree(tuple[
                                                                           1])
                            print(answer_tree)

            print("\n\n")

        # trees = [Tree.fromstring(line) for line in sentences]
        print()  # new line per question
    sys.stdout = orig_stdout
    f.close()

if __name__ == '__main__':
    input_file_name = sys.argv[1]
    story_list = read_file(input_file_name)
    process_command(story_list)
