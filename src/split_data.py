import sys, os
import pdb
from collections import OrderedDict
import unicodedata
import time
import re

class SentenceData:
	def __init__(self, sentence, normalized_sentence, label=None):
		self.sentence = sentence
		self.normalized_sentence = normalized_sentence
		self.label = label
		
class PhraseData:
	def __init__(self, phrase, normalized_phrase, label=None, sentence_ids=[]):
		self.phrase = phrase
		self.normalized_phrase = normalized_phrase
		self.label = label

def normalize(text):
	text = text.replace('(', '-LRB-')
	text = text.replace(')', '-RRB-')
	text = re.sub(r'[^\x00-\x7F]+',' ', text)
	#uText = unicode(text, "UTF-8")
	#text = unicodedata.normalize('NFD', uText).encode('ascii', 'ignore')
	return text

def get_split_dict(datasetSplit):
	split_dict = {}
	i = 0
	for line in datasetSplit.readlines():
		if i == 0:
			i += 1
			continue
		index, split = line.strip().split(',')
		split_dict[index] = split
	return split_dict

def get_sentence_data(datasetSentences):
	train_sentence_data = OrderedDict()
	test_sentence_data = OrderedDict()
	dev_sentence_data = OrderedDict()
	i = 0
	for line in datasetSentences.readlines():
		if i == 0:
			i += 1
			continue
		index, sentence = line.strip().split('\t')
		normalized_sentence = normalize(sentence)
		if split_dict[index] == '1':
			train_sentence_data[index] = SentenceData(sentence, normalized_sentence)
		elif split_dict[index] == '2':
			test_sentence_data[index] = SentenceData(sentence, normalized_sentence)
		elif split_dict[index] == '3':
			dev_sentence_data[index] = SentenceData(sentence, normalized_sentence)
	return train_sentence_data, test_sentence_data, dev_sentence_data
	
def update_data(phrase_data, split_sentence_data):
	found = False
	for sentence_id in split_sentence_data:
		if phrase_data.normalized_phrase in split_sentence_data[sentence_id].normalized_sentence:
			found = True
			if phrase_data.normalized_phrase == split_sentence_data[sentence_id].normalized_sentence:
				split_sentence_data[sentence_id].label = phrase_data.label 
	return found
		
def get_phrase_data(datasetPhrases, sentiment_labels, train_sentence_data, test_sentence_data, dev_sentence_data):
	train_phrase_data = OrderedDict()
	test_phrase_data = OrderedDict()
	dev_phrase_data = OrderedDict()
	i = 0
	for line in datasetPhrases.readlines():
		phrase, index = line.strip().split('|')
		normalized_phrase = normalize(phrase)
		phrase_data = PhraseData(phrase, normalized_phrase, sentiment_labels[index])
		if update_data(phrase_data, train_sentence_data):
			train_phrase_data[index] = phrase_data
		if update_data(phrase_data, test_sentence_data):
			test_phrase_data[index] = phrase_data
		if update_data(phrase_data, dev_sentence_data):
			dev_phrase_data[index] = phrase_data
	return train_phrase_data, test_phrase_data, dev_phrase_data
	
def get_sentiment_labels(sentimentLabels):
	sentiment_labels = {}
	i = 0
	for line in sentimentLabels.readlines():
		if i == 0:
			i += 1
			continue
		index, label = line.strip().split('|')
		sentiment_labels[index] = label
	return sentiment_labels

def write_data(sentence_data, phrase_data, folder):
	sentence_file = open(os.path.join(folder, "datasetSentences.txt"), 'w')
	sentence_file.write("sentence_id\tsentence\tsentiment_label\tpositivity_probability\n")
	for index in sentence_data:
		if sentence_data[index].label == None:
			print 'TRAIN OR DEV'
			print sentence_data[index].sentence
			#pdb.set_trace()
		if float(sentence_data[index].label) <= 0.4:
			sentiment_label = "-1"
		elif float(sentence_data[index].label) >= 0.6:
			sentiment_label = "+1"
		else:
			sentiment_label = "0"
		sentence_file.write("%s\t%s\t%s\t%s\n" % (index,sentence_data[index].sentence, sentiment_label, sentence_data[index].label))
	
	phrase_file = open(os.path.join(folder, "datasetPhrases.txt"), 'w')
	phrase_file.write("phrase_id\tphrase\tsentiment_label\tpositivity_probability\n")
	for index in phrase_data:
		if float(phrase_data[index].label) <= 0.4:
			sentiment_label = "-1"
		elif float(phrase_data[index].label) >= 0.6:
			sentiment_label = "+1"
		else:
			sentiment_label = "0"
		phrase_file.write("%s\t%s\t%s\t%s\n" % (index, phrase_data[index].phrase, sentiment_label, phrase_data[index].label))

def write_test_data(sentence_data, phrase_data, folder):
	sentence_file = open(os.path.join(folder, "datasetSentences.txt"), 'w')
	sentence_labels_file = open(os.path.join(folder, "datasetSentenceLabels.txt"), 'w')
	sentence_file.write("sentence_id\tsentence\n")
	sentence_labels_file.write("sentence_id\tsentiment_label\tpositivity_probability\n")
	for index in sentence_data:
		if sentence_data[index].label == None:
			print 'TEST'
			print sentence_data[index].sentence
		if float(sentence_data[index].label) <= 0.4:
			sentiment_label = "-1"
		elif float(sentence_data[index].label) >= 0.6:
			sentiment_label = "+1"
		else:
			sentiment_label = "0"
		sentence_file.write("%s\t%s\n" % (index, sentence_data[index].sentence))
		sentence_labels_file.write("%s\t%s\t%s\n" %(index, sentiment_label, sentence_data[index].label))
	
	phrase_file = open(os.path.join(folder, "datasetPhrases.txt"), 'w')
	phrase_labels_file = open(os.path.join(folder, "datasetPhraseLabels.txt"), 'w')
	phrase_file.write("phraseId\tPhrase\n")
	phrase_labels_file.write("phraseId\tsentiment_label\tpositivity_probability\n")
	for index in phrase_data:
		if phrase_data[index].label <= 0.4:
			sentiment_label = "-1"
		elif phrase_data[index].label >= 0.6:
			sentiment_label = "+1"
		else:
			sentiment_label = "0"
		phrase_file.write("%s\t%s\n" % (index, phrase_data[index].phrase))
		phrase_labels_file.write("%s\t%s\t%s\n" % (index, sentiment_label, phrase_data[index].label))

if __name__ == "__main__":
	datasetSentences = open(sys.argv[1], 'r')
	datasetSplit = open(sys.argv[2], 'r')
	sentimentLabels = open(sys.argv[3], 'r')
	datasetPhrases = open(sys.argv[4], 'r')
	
	train_folder = sys.argv[5]
	dev_folder = sys.argv[6]
	test_folder = sys.argv[7]
	
	split_dict = get_split_dict(datasetSplit)
	
	start_time = time.time()
	print 'get_sentence_data'
	train_sentence_data, test_sentence_data, dev_sentence_data = get_sentence_data(datasetSentences)
	print 'Done! Time taken ', time.time() - start_time
	print
	start_time = time.time()
	print 'get_phrase_sentiment_labels'
	sentiment_labels = get_sentiment_labels(sentimentLabels)
	print 'Done! Time taken ', time.time() - start_time
	print
	start_time = time.time()
	print 'get_phrase_data'
	train_phrase_data, test_phrase_data, dev_phrase_data = get_phrase_data(datasetPhrases, sentiment_labels, \
																		   train_sentence_data, test_sentence_data, dev_sentence_data)
	print 'Done! Time taken ', time.time() - start_time
	print
	start_time = time.time()
	print 'writing data..'
	write_data(train_sentence_data, train_phrase_data, train_folder)
	write_test_data(test_sentence_data, test_phrase_data, test_folder)
	write_test_data(dev_sentence_data, dev_phrase_data, dev_folder)
	print 'Done! Time taken ', time.time() - start_time
	print
		
			
	
