import constituency_demo_stub
import read_write_stub
from nltk.tree import Tree
import nltk
import sys

def read_file(file_name):
	story_ids = []
	f = open(file_name, 'r')
	text = f.read()
	f.close()

	for line in text.split('\n'):
		story_ids.append(line)

	return story_ids

if __name__ == '__main__':
	input_file_name = sys.argv[1]
	story_ids = read_file(input_file_name)
	print(story_ids)

	for fname in story_ids:
		print(fname)
		data_dict = read_write_stub.get_data_dict(fname)
		questions = read_write_stub.getQA("{}.questions".format(fname))
		print(len(questions))
		for q in range(0,len(questions)):
			qname = "{0}-{1}".format(fname, q+1)
			qtypes = questions[qname]['Type']
			print(qtypes)
			# qtypes can be "Story", "Sch", "Sch | Story"
			for qt in qtypes.split("|"):
				qt = qt.strip().lower()
				# These are the text data where you can look for answers.
				raw_text = data_dict[qt]
				par_text = data_dict[qt + ".par"]

				sentences = []
				for line in par_text.split('\n'):
					sentences.append(line)
				print(sentences)
				#print(par_text)
				#trees = [Tree.fromstring(line) for line in sentences]
		print()

