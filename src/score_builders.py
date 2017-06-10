import sys
import pdb
from sklearn.metrics import classification_report

if __name__ == '__main__':
    predictions_file = open(sys.argv[1], 'r')
    ground_truth_file = open(sys.argv[2], 'r')
    predicted_labels = {}
    true_labels = {}
    for line in predictions_file.readlines():
        if '\t' in line:
            id, sentence, label = line.split('\t')
        else:
            id = line.split()[0]
            label = line.split()[-1]
        if 'sentence_id' in id:
            continue
        predicted_labels[id] = float(label)
    for line in ground_truth_file.readlines():
        id, sentence, label = line.split('\t')
        if 'sentence_id' in id:
            continue
        true_labels[id] = float(label)
    predicted = []
    true = []
    for id in predicted_labels.keys():
        predicted.append(predicted_labels[id])
        true.append(true_labels[id])
    target_names = ['-1', '0', '1']
    print(classification_report(true, predicted, target_names=target_names))
    