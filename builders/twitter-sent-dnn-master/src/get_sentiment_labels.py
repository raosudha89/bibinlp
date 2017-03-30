import sys, pdb
import argparse
sys.path.insert(0, '/fs/clip-amr/bibinlp/builders/twitter-sent-dnn-master/model')
from sentiment import sentiment_score

def main(args):
	if args.split == 'test' or args.split == 'dev':
		evaluate_test(args)
	elif args.split == 'train':
		evaluate_train(args)
	
def evaluate_train(args):
	sentences_file = open(args.sentences_file, 'r')
	output_labels_file = open(args.output_labels_file, 'w')
	i = 0
	for line in sentences_file.readlines():
		if i == 0:
			output_labels_file.write('sentence_id\tsentence\ttrue_sentiment\tpredicted_sentiment\n')
			i += 1
			continue
		index, sentence, label, _ = line.split('\t')
		score = sentiment_score(sentence)
		if score <= 0.4:
			predicted_label = '-1'
		elif score >= 0.6:
			predicted_label = '+1'
		else:
			predicted_label = '0'
		output_labels_file.write('%s\t%s\t%s\t%s\n' % (index, sentence, label, predicted_label))
	
def evaluate_test(args):
	sentences_file = open(args.sentences_file, 'r')
	labels_file = open(args.labels_file, 'r')
	output_labels_file = open(args.output_labels_file, 'w')
	sentences_lines = sentences_file.readlines()
	labels_lines = labels_file.readlines()
	output_labels_file.write('sentence_id\tsentence\ttrue_sentiment\tpredicted_sentiment\n')
	for i in range(1, len(sentences_lines)):
		index, sentence = sentences_lines[i].split('\t')
		_, label, _ = labels_lines[i].split('\t')
		sentence = sentence.strip('\n')
		score = sentiment_score(sentence)
		if score <= 0.4:
			predicted_label = '-1'
		elif score >= 0.6:
			predicted_label = '+1'
		else:
			predicted_label = '0'
		output_labels_file.write('%s\t%s\t%s\t%s\n' % (index, sentence, label, predicted_label))

if __name__ == '__main__':
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--split", type = str)
	argparser.add_argument("--sentences_file", type = str)
	argparser.add_argument("--labels_file", type = str)
	argparser.add_argument("--output_labels_file", type=str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)
