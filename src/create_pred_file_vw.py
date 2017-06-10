import sys

if __name__ == '__main__':
    predictions_file = open(sys.argv[1], 'r')
    truth_file = open(sys.argv[2], 'r')
    new_predictions_file = open(sys.argv[3], 'w')
    pred_labels = []
    for line in predictions_file.readlines():
        pred_labels.append(line.strip('\n'))
    i = 0
    for line in truth_file.readlines():
        if i == 0:
            i += 1
            continue
        id, sentence, _ = line.split('\t')
        new_predictions_file.write('\t'.join([id, sentence, pred_labels[i-1]])+'\n')
        i += 1