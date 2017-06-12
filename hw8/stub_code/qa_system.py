import constituency_demo_stub
import read_write_stub
from nltk.tree import Tree
import nltk
import baseline_stub
from baseline_stub import get_sentences
from baseline_stub import get_bow
# baseline_stub_word2vec_demo imports
from word2vec_extractor import Word2vecExtractor
from sklearn.metrics.pairwise import cosine_similarity
from dependency_demo_stub import read_dep_parses, find_main
from baseline_stub_word2vec_demo import get_word2vec_answers
import sys
import random
import operator
from collections import Counter


def read_file(file_name):
    # getting the correct story files
    story_ids = []
    f = open(file_name, 'r')
    lines = f.readlines()
    for line in lines:
        story_ids.append(line.rstrip('\n'))
    f.close()
    return story_ids


def get_question_parse_tree(qname, par_raw):
    question_par_dict = {}  # {QID: parse_tree}
    parse_raw_list = par_raw.split("\n")
    for line in parse_raw_list:
        if not line:
            pass
        else:  # line is not empty string
            if line[0] == 'Q':
                parse_ID = line[12:]  # get only ID string
            elif line[0] == '(':
                parse_line = line
                question_par_dict[parse_ID] = parse_line
    for key, tree in question_par_dict.items():
        if qname == key:
            question_parse_tree = constituency_demo_stub.make_tree(tree)
            return question_parse_tree
    return None


def most_common(lst):
    return max(lst, key=lst.count)


def find_best_candidate(candidates):
    candidate_list = []
    for answer_list in candidates:
        if answer_list is not None:
            for answer in answer_list:
                candidate_list.append(answer)
    # best_answer = max(candidate_dict.iteritems(),
    #                   key=operator.itemgetter(1))[0]
    best_answer = most_common(candidate_list)
    return best_answer


def get_answer_parse_tree(qtypes, data_dict, question, fname):
    # IN: qt, data_dict
    # OUT: tree_tuple
    stopwords = set(nltk.corpus.stopwords.words("english"))
    answer_list = []
    wait = False
    make_tuple = False

    for qt in qtypes.split("|"):
        if len(qtypes.split("|")) > 1:
            wait = True
        qt = qt.strip().lower()
        raw_text = data_dict[qt]
        par_text = data_dict[qt + ".par"]
        raw_text_list = get_sentences(raw_text)
        par_text_list = par_text.split("\n")
        par_text_list = filter(None, par_text_list)
        raw_par_list = []
        for r, p in zip(raw_text_list, par_text_list):
            raw_par_list.append((r, p))
        qbow = get_bow(get_sentences(question)[0], stopwords)
        # baseline answers
        baseline_answers = baseline_stub.baseline(
            qbow, raw_text_list, stopwords)
        # stem answers
        stem_answers = baseline_stub.stem_baseline(
            qbow, raw_text_list, stopwords)
        # wordnet answers
        wordnet_answers = baseline_stub.wordnet_baseline(
            question, raw_text_list, stopwords)
        # word2vec answers
        dep_fname = fname + ".questions.dep"
        print(dep_fname)
        word2vec_answers = get_word2vec_answers(
            question, dep_fname, raw_text)
        answer_candidates = [baseline_answers,
                             stem_answers, wordnet_answers, word2vec_answers]
        answer = find_best_candidate(answer_candidates)
        answer_string = " ".join(t[0] for t in answer)
        for tuple in raw_par_list:
            if tuple[0] == answer:
                if wait:
                    tree_sch = constituency_demo_stub.make_tree(tuple[1])
                    wait = False
                    make_tuple = True
                answer_tree = constituency_demo_stub.make_tree(tuple[1])
    if make_tuple:
        return (tree_sch, answer_tree)
    else:
        return answer_tree


def get_question_type(qtree):
    # Who, What
    wp_pattern = nltk.ParentedTree.fromstring("(WP)")
    # Where When How Why
    wrb_pattern = nltk.ParentedTree.fromstring("(WRB)")
    # WHAT in a group of trees blogs-02-12
    wdt_pattern = nltk.ParentedTree.fromstring("(WDT)")
    # subtrees
    wp_subtree = constituency_demo_stub.pattern_matcher(wp_pattern, qtree)
    wrb_subtree = constituency_demo_stub.pattern_matcher(wrb_pattern, qtree)
    wdt_subtree = constituency_demo_stub.pattern_matcher(wdt_pattern, qtree)
    if wp_subtree is not None:
        return " ".join(wp_subtree.leaves())
    elif wrb_subtree is not None:
        return " ".join(wrb_subtree.leaves())
    elif wdt_subtree is not None:
        return " ".join(wdt_subtree.leaves())


def find_phrase(question_type, answer_tree):
    answer_dict = {}
    answer_dict['Who'] = ['(S(NP))', '(NP)', '(NN)']
    # sort of works
    answer_dict['What'] = ['(S(NP)(*)(VP))', '(VP(*)(PP))']
    # answer_dict['What'] = ['(S(NP)(*)(VP))','(VP(*)(PP))','((*)(NP))']
    answer_dict['Where'] = ['(S(*(PP)))', '(PP)']
    answer_dict['When'] = ['(S(WHADVP))', '(S(ADVP))']
    # answer_dict['How'] = ['(S(*)(*)(CC)(VP))', '(VP(VBD))']
    answer_dict['How'] = ['(S)']
    answer_dict['Why'] = ['(SBAR)']
    answer_grammar_list = answer_dict[question_type]
    none_count = 0
    current_tree = answer_tree  # base case
    # while none_count != len(answer_grammar_list):
    for grammar in answer_grammar_list:
        pattern = nltk.ParentedTree.fromstring(grammar)
        check_tree = constituency_demo_stub.pattern_matcher(
            pattern, current_tree)
        if check_tree is not None:
            current_tree = check_tree
        else:  # check_tree returned NONE
            pass
    return " ".join(current_tree.leaves())


def process_command(story_list):
    # IN: story_id.txt from command line
    # OUT:
    # orig_stdout = sys.stdout
    # 'lastname1_lastname2_answers.txt'
    out_filename = "chien_lee_answers.txt"
    f = open(out_filename, 'w')
    # sys.stdout = f
    # Iterate through each story file
    for fname in story_list:
        data_dict = read_write_stub.get_data_dict(fname)
        questions = read_write_stub.getQA("{}.questions".format(fname))
        for q in range(0, len(questions)):
            qname = "{0}-{1}".format(fname, q + 1)
            f.write("QuestionID: " + qname + "\n")
            qtypes = questions[qname]['Type']
            # print("QuestionType: " + qtypes)
            question = questions[qname]['Question']
            print("Question String: " + question)

            # QUESTION PARSE TREE
            question_parse_tree = get_question_parse_tree(
                qname, data_dict["questions.par"])
            question_type = get_question_type(question_parse_tree)
            # print("Question Parse Tree: {}\n".format(question_parse_tree))
            # print("WH WORD: {}".format(question_type))

            # LIST OF ANSWER PARSE TREES (sch|story) only
            answer_parse_tree_data = get_answer_parse_tree(
                qtypes, data_dict, question, fname)
            # IF WE HAVE AN SCH|STORY
            # print("Answer Parse Tree: {}\n".format(answer_parse_tree_data))
            if isinstance(answer_parse_tree_data, tuple):
                answer_phrase_sch = find_phrase(
                    question_type, answer_parse_tree_data[0])
                answer_phrase_story = find_phrase(
                    question_type, answer_parse_tree_data[1])
                # FLIP A COIN FOR ONE OUTPUT ONLY SMH
                if random.random() > 0.5:
                    f.write("Answer: {}\n\n".format(answer_phrase_sch))
                    print("Answer: {}".format(answer_phrase_sch))
                else:
                    f.write("Answer: {}\n\n".format(answer_phrase_story))
                    print("Answer: {}".format(answer_phrase_story))
            # IT'S EITHER ONLY SCH OR ONLY STORY
            else:
                answer_phrase = find_phrase(
                    question_type, answer_parse_tree_data)
                # print(answer_tree)
                f.write("Answer: {}\n\n".format(answer_phrase))
                print("Answer: {}".format(answer_phrase))
                # print(answer_phrase)
            print()  # new line per question
    # sys.stdout = orig_stdout
    f.close()

if __name__ == '__main__':
    input_file_name = sys.argv[1]
    story_list = read_file(input_file_name)
    process_command(story_list)
