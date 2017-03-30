import sys, pdb
import argparse
from collections import defaultdict

def main(args):
	if args.split == 'test' or args.split == 'dev':
		evaluate_test(args)
	elif args.split == 'train':
		evaluate_train(args)

def read_predictions(predictions_file, num):
	i = 0
	predicted_labels = [None]*num
	predicted_sentiments = defaultdict(list)
	for line in predictions_file.readlines():
		index, label = line.split()
		index = index.split('_')[1]
		predicted_sentiments[int(index)].append(label.strip())
	for index in predicted_sentiments:
		p = predicted_sentiments[index].count('positive')
		n = predicted_sentiments[index].count('negative')
		if p > n:
			predicted_labels[index-1] = '+1'
		elif p < n:
			predicted_labels[index-1] = '-1'
		else:
			predicted_labels[index-1] = '0'	
	return predicted_labels

def evaluate_train(args):
	predictions_file = open(args.predictions_file, 'r')
	sentences_file = open(args.sentences_file, 'r')
	output_labels_file = open(args.output_labels_file, 'w')
	sentences_lines = sentences_file.readlines()
	predicted_labels = read_predictions(predictions_file, len(sentences_lines)-1)
	output_labels_file.write("sentence_id\tsentence\ttrue_sentiment\tpredicted_sentiment\n")
	for i in range(1, len(sentences_lines)):
		index, sentence, label, _ = sentences_lines[i].split('\t')
		output_labels_file.write("%s\t%s\t%s\t%s\n" % (index, sentence, label, predicted_labels[i-1]))

def evaluate_test(args):
	predictions_file = open(args.predictions_file, 'r')
	sentences_file = open(args.sentences_file, 'r')
	labels_file = open(args.labels_file, 'r')
	output_labels_file = open(args.output_labels_file, 'w')
	sentences_lines = sentences_file.readlines()
	labels_lines = labels_file.readlines()
	predicted_labels = read_predictions(predictions_file, len(sentences_lines)-1)
	output_labels_file.write("sentence_id\tsentence\ttrue_sentiment\tpredicted_sentiment\n")
	for i in range(1, len(sentences_lines)):
		index, sentence = sentences_lines[i].split('\t')
		_, label, _ = labels_lines[i].split('\t')
		sentence = sentence.strip('\n')
		output_labels_file.write("%s\t%s\t%s\t%s\n" % (index, sentence, label, predicted_labels[i-1]))

if __name__ == '__main__':
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--split", type = str)
	argparser.add_argument("--sentences_file", type = str)
	argparser.add_argument("--labels_file", type = str)
	argparser.add_argument("--predictions_file", type = str)
	argparser.add_argument("--output_labels_file", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)
