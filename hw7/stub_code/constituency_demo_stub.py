#!/usr/bin/env python
'''
Created on May 14, 2014
@author: reid

Modified on May 21, 2015
'''

import sys
import nltk
from nltk.tree import Tree


def process_question_file(parfile):
    # IN: .par filename
    # OUT: list of trees
    question_list = read_question(parfile)
    tree_list = []
    for line in question_list:
        tree_list.append(make_tree(line))
    # print(tree_list)
    return tree_list


def read_question(parfile):
    # IN: .par filename
    # OUT: list of strings with parse text
    fh = open(parfile, 'r')
    lines = fh.readlines()
    fh.close()
    question_list = []
    for line in lines:
        if line[0] == '(':
            question_list.append(line)
            # print(line)
    return question_list


def make_tree(line):
    # IN: string line
    # OUT: tree
    return Tree.fromstring(line)


# Read the constituency parse from the line and construct the Tree
def read_con_parses(parfile):
    tree_list = []
    fh = open(parfile, 'r')
    lines = fh.readlines()
    fh.close()
    # for line in lines:
    #     if line[0] == '(':
    #         tree_one = Tree.fromstring(line)
    #         tree_list.append(tree_one)
    # return tree_list
    return [Tree.fromstring(line) for line in lines]

# See if our pattern matches the current root of the tree


def matches(pattern, root):
    # Base cases to exit our recursion
    # If both nodes are null we've matched everything so far
    if root is None and pattern is None:
        return root

    # We've matched everything in the pattern we're supposed to (we can ignore the extra
    # nodes in the main tree for now)
    elif pattern is None:
        return root

    # We still have something in our pattern, but there's nothing to match in
    # the tree
    elif root is None:
        return None

    # A node in a tree can either be a string (if it is a leaf) or node
    plabel = pattern if isinstance(pattern, str) else pattern.label()
    rlabel = root if isinstance(root, str) else root.label()

    # If our pattern label is the * then match no matter what
    if plabel == "*":
        return root
    # Otherwise they labels need to match
    elif plabel == rlabel:
        # If there is a match we need to check that all the children match
        # Minor bug (what happens if the pattern has more children than the
        # tree)
        for pchild, rchild in zip(pattern, root):
            match = matches(pchild, rchild)
            if match is None:
                return None
        return root

    return None


def pattern_matcher(pattern, tree):
    for subtree in tree.subtrees():
        node = matches(pattern, subtree)
        if node is not None:
            return node
    return None

if __name__ == '__main__':
    text_file = "fables-01.sch"
    par_file = "fables-01.sch.par"

    # Read the constituency parses into a list
    trees = read_con_parses(par_file)

    # We choose trees[1] because we already know that the answer we're looking
    # for is in the second sentence of the text
    tree = trees[1]

    # Create our pattern
    pattern = nltk.ParentedTree.fromstring("(VP (*) (PP))")

    # # Match our pattern to the tree
    subtree = pattern_matcher(pattern, tree)
    print(" ".join(subtree.leaves()))

    # create a new pattern to match a smaller subset of subtree
    pattern = nltk.ParentedTree.fromstring("(PP)")

    # Find and print the answer
    subtree2 = pattern_matcher(pattern, subtree)
    print(" ".join(subtree2.leaves()))
