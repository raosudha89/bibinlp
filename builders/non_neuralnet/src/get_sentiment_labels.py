import sys, pdb
import argparse

def main(args):
	sentences_file = open(args.sentences_file, 'r')
	labels_file = open(args.labels_file, 'r')
	predictions_file = open(args.predictions_file, 'r')
	output_labels_file = open(args.output_labels_file, 'w')
	sentences_lines = sentences_file.readlines()
	labels_lines = labels_file.readlines()
	predictions_lines = predictions_file.readlines()
	output_labels_file.write('sentence_id\tsentence\ttrue_sentiment\tpredicted_sentiment\n')
	for i in range(1, len(sentences_lines)):
		sent_index, sentence = sentences_lines[i].split('\t')
		label_index, label, _ = labels_lines[i].split('\t')
		sentence = sentence.strip('\n')
		pred_label_index, predicted_label, _ = predictions_lines[i-1].split('\t')
		if predicted_label == '1':
			predicted_label = '+1'
		assert(sent_index == label_index)
		assert(pred_label_index == label_index)
		output_labels_file.write('%s\t%s\t%s\t%s\n' % (sent_index, sentence, label, predicted_label))

if __name__ == '__main__':
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--sentences_file", type = str)
	argparser.add_argument("--labels_file", type = str)
	argparser.add_argument("--predictions_file", type = str)
	argparser.add_argument("--output_labels_file", type=str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)
