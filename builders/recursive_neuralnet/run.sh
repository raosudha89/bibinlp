java -cp '/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0.jar:/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0-models.jar:/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/ejml-0.23.jar' edu.stanford.nlp.sentiment.SentimentPipeline -file dev/datasetSentences.in > dev/datasetSentences.out &
java -cp '/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0.jar:/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0-models.jar:/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/ejml-0.23.jar' edu.stanford.nlp.sentiment.SentimentPipeline -file train/datasetSentences.in > train/datasetSentences.out &
java -cp '/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0.jar:/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0-models.jar:/fs/clip-software/user-supported/stanford-corenlp-full-2016-10-31/ejml-0.23.jar' edu.stanford.nlp.sentiment.SentimentPipeline -file test/datasetSentences.in > test/datasetSentences.out &

python src/evaluate.py --predictions_file dev/datasetSentences.out --sentences_file ../../dev/datasetSentences.txt --labels_file ../../dev/datasetSentenceLabels.txt --split dev 
Namespace(labels_file='../../dev/datasetSentenceLabels.txt', predictions_file='dev/datasetSentences.out', sentences_file='../../dev/datasetSentences.txt')

Correct:  [350, 45, 331]
Total:  [428, 229, 444]
Negative Acc:  0.817757009346
Neutral Acc:  0.196506550218
Positive Acc:  0.745495495495

Acc:  0.659400544959

python src/evaluate.py --predictions_file test/datasetSentences.out --sentences_file ../../test/datasetSentences.txt --labels_file ../../test/datasetSentenceLabels.txt --split test 
Namespace(labels_file='../../test/datasetSentenceLabels.txt', predictions_file='test/datasetSentences.out', sentences_file='../../test/datasetSentences.txt')

Correct:  [712, 85, 685]
Total:  [912, 390, 908]
Negative Acc:  0.780701754386
Neutral Acc:  0.217948717949
Positive Acc:  0.754405286344

Acc:  0.670588235294

python src/evaluate.py --predictions_file train/datasetSentences.out --sentences_file ../../train/datasetSentences.txt --split train
Namespace(labels_file=None, predictions_file='train/datasetSentences.out', sentences_file='../../train/datasetSentences.txt', split='train')

Correct:  [2950, 492, 3089]
Total:  [3310, 1624, 3610]
Negative Acc:  0.891238670695
Neutral Acc:  0.302955665025
Positive Acc:  0.85567867036

Acc:  0.764396067416
