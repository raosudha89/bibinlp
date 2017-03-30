import sys, pdb
import argparse

def main(args):
	if args.split == 'test' or args.split == 'dev':
		evaluate_test(args)
	elif args.split == 'train':
		evaluate_train(args)

def read_predictions(predictions_file, sentences):
	i = 0
	predicted_labels = []
	for line in predictions_file.readlines():
		if i % 2 == 0:
			sentence = line.strip("\n")
			if sentences[i/2] != sentence:
				pdb.set_trace()
		elif i % 2 == 1:
			if '  ' == line[:2]:
				label = line[2:].strip("\n")
				if 'Positive' in label or 'Very positive' in label:
					predicted_labels.append("+1")
				elif 'Negative' in label or 'Very negative' in label:
					predicted_labels.append("-1")
				else:
					predicted_labels.append("0")
			else: # label is missing
				predicted_labels.append("0")
				i += 1
				sentence = line.strip("\n")
				assert(sentences[i/2] == sentence)
		i += 1
	return predicted_labels

def evaluate_train(args):
	predictions_file = open(args.predictions_file, 'r')
	sentences_file = open(args.sentences_file, 'r')
	output_labels_file = open(args.output_labels_file, 'w')
	indices = []
	sentences = []
	i = 0
	for line in sentences_file.readlines():
		if i == 0:
			i += 1
			continue
		index, sentence, label, _ = line.split('\t')
		indices.append(index)
		sentences.append(sentence.strip("\n"))  
	predicted_labels = read_predictions(predictions_file, sentences)
	assert(len(indices) == len(predicted_labels))
	write_predictions(indices, sentences, predicted_labels, output_labels_file)

def evaluate_test(args):
	predictions_file = open(args.predictions_file, 'r')
	sentences_file = open(args.sentences_file, 'r')
	labels_file = open(args.labels_file, 'r')
	output_labels_file = open(args.output_labels_file, 'w')
	indices = []
	sentences = []
	labels = []
	sentences_lines = sentences_file.readlines()
	labels_lines = labels_file.readlines()
	for i in range(1, len(sentences_lines)):
		index, sentence = sentences_lines[i].split('\t')
		_, label, _ = labels_lines[i].split('\t')
		indices.append(index)
		sentences.append(sentence.strip("\n"))
		labels.append(label)
	predicted_labels = read_predictions(predictions_file, sentences)
	assert(len(indices) == len(predicted_labels))
	write_predictions(indices, sentences, labels, predicted_labels, output_labels_file)

def write_predictions(indices, sentences, labels, predicted_labels, output_labels_file):
	output_labels_file.write('sentence_id\tsentence\ttrue_sentiment\tpredicted_sentiment\n')
	for i in range(len(predicted_labels)):
		output_labels_file.write("%s\t%s\t%s\t%s\n" % (indices[i], sentences[i], labels[i], predicted_labels[i]))

if __name__ == '__main__':
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--split", type = str)
	argparser.add_argument("--predictions_file", type = str)
	argparser.add_argument("--sentences_file", type = str)
	argparser.add_argument("--labels_file", type = str)
	argparser.add_argument("--output_labels_file", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)


