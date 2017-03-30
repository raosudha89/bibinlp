python run_sentiment_model.py --sentences_file /fs/clip-amr/bibinlp/blindDev/datasetSentences.txt --labels_file /fs/clip-amr/bibinlp/blindDev/datasetSentenceLabels.txt --split dev 
Namespace(labels_file='/fs/clip-amr/bibinlp/blindDev/datasetSentenceLabels.txt', sentences_file='/fs/clip-amr/bibinlp/blindDev/datasetSentences.txt')

Correct:  [323, 14, 337]
Total:  [428, 229, 444]
Negative Acc:  0.754672897196
Neutral Acc:  0.061135371179
Positive Acc:  0.759009009009

Acc:  0.61217075386

python run_sentiment_model.py --sentences_file /fs/clip-amr/bibinlp/blindTest/datasetSentences.txt --labels_file /fs/clip-amr/bibinlp/blindTest/datasetSentenceLabels.txt --split test 
Namespace(labels_file='/fs/clip-amr/bibinlp/blindTest/datasetSentenceLabels.txt', sentences_file='/fs/clip-amr/bibinlp/blindTest/datasetSentences.txt')

Correct:  [690, 27, 685]
Total:  [912, 390, 908]
Negative Acc:  0.756578947368
Neutral Acc:  0.0692307692308
Positive Acc:  0.754405286344

Acc:  0.634389140271

python run_sentiment_model.py --sentences_file /fs/clip-amr/bibinlp/train/datasetSentences.txt --split train
Namespace(labels_file=None, sentences_file='/fs/clip-amr/bibinlp/train/datasetSentences.txt', split='train')

Correct:  [2759, 88, 2904]
Total:  [3310, 1624, 3610]
Negative Acc:  0.833534743202
Neutral Acc:  0.0541871921182
Positive Acc:  0.804432132964

Acc:  0.673103932584
