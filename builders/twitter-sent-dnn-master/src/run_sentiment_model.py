import sys, pdb
import argparse
from sentiment import sentiment_score

def main(args):
	if args.split == 'test' or args.split == 'dev':
		evaluate_test(args)
	elif args.split == 'train':
		evaluate_train(args)

def print_results(corr, total):
	print 'Correct: ', corr
	print 'Total: ', total
	print 'Negative Acc: ', corr[0]*1.0/total[0]
	print 'Neutral Acc: ', corr[1]*1.0/total[1]
	print 'Positive Acc: ', corr[2]*1.0/total[2]
	print
	print 'Acc: ', (corr[0] + corr[1] + corr[2])*1.0/(total[0] + total[1] + total[2])
	
def evaluate_train(args):
	sentences_file = open(args.sentences_file, 'r')
	i = 0
	corr = [0, 0, 0]
	total = [0, 0, 0]
	for line in sentences_file.readlines():
		if i == 0:
			i += 1
			continue
		_, sentence, label, _ = line.split('\t')
		score = sentiment_score(sentence)
		if label == '-1':
			if score <= 0.4:
				corr[0] += 1
			total[0] += 1
		elif label == '0':
			if score > 0.4 and score < 0.6:
				corr[1] += 1
			total[1] += 1
		elif label == '+1':
			if score >= 0.6:
				corr[2] += 1
			total[2] += 1
	print_results(corr, total)
	
def evaluate_test(args):
	sentences_file = open(args.sentences_file, 'r')
	labels_file = open(args.labels_file, 'r')
	scores = []
	i = 0
	for line in sentences_file.readlines():
		if i == 0:
			i += 1
			continue
		_, sentence = line.split('\t')
		score = sentiment_score(sentence.strip('\n'))
		scores.append(score)
	corr = [0, 0, 0]
	total = [0, 0, 0]
	i = -1
	for line in labels_file.readlines():
		if i == -1:
			i += 1
			continue
		_, label, _ = line.split('\t')
		if label == '-1':
			if scores[i] <= 0.4:
				corr[0] += 1
			total[0] += 1
		elif label == '0':
			if scores[i] > 0.4 and scores[i] < 0.6:
				corr[1] += 1
			total[1] += 1
		elif label == '+1':
			if scores[i] >= 0.6:
				corr[2] += 1
			total[2] += 1
		i += 1
	print_results(corr, total)
	create_predictions_output_file()

if __name__ == '__main__':
	argparser = argparse.ArgumentParser(sys.argv[0])
	argparser.add_argument("--split", type = str)
	argparser.add_argument("--sentences_file", type = str)
	argparser.add_argument("--labels_file", type = str)
	args = argparser.parse_args()
	print args
	print ""
	main(args)


