import sys

if __name__ == '__main__':
    sentences_file = open(sys.argv[1], 'r')
    out_file = open(sys.argv[2], 'w')
    i = 0
    for line in sentences_file.readlines():
        if i == 0:
            i += 1
            continue
        splits = line.split('\t')
        index, sentence = splits[0], splits[1]
        sentence = sentence.strip("\n")
        out_file.write(sentence + "\n")
        
