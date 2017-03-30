for i in {1..8544}; do sed -n $i,${i}p ../recursive_neuralnet/train/datasetSentences.in > train/$i; done
for i in {1..2210}; do sed -n $i,${i}p ../recursive_neuralnet/test/datasetSentences.in > test/$i; done
for i in {1..1101}; do sed -n $i,${i}p ../recursive_neuralnet/dev/datasetSentences.in > dev/$i; done

for i in {1..8544}; do java -cp lib/stanford-postagger.jar:lib/weka.jar:opinionfinder.jar opin.main.RunOpinionFinder train/$i; done > train_run.out 2>&1 &
for i in {1..2210}; do java -cp lib/stanford-postagger.jar:lib/weka.jar:opinionfinder.jar opin.main.RunOpinionFinder test/$i; done > test_run.out 2>&1 &
for i in {1..1101}; do java -cp lib/stanford-postagger.jar:lib/weka.jar:opinionfinder.jar opin.main.RunOpinionFinder dev/$i; done > dev_run.out 2>&1 &

for i in {1..8544}; do cat train/${i}_auto_anns/exp_polarity.txt >> train/datasetSentences.out; done
for i in {1..2210}; do cat test/${i}_auto_anns/exp_polarity.txt >> test/datasetSentences.out; done
for i in {1..1101}; do cat dev/${i}_auto_anns/exp_polarity.txt >> dev/datasetSentences.out; done

python evaluate.py --predictions_file dev/datasetSentences.out --labels_file /fs/clip-amr/bibinlp/blindDev/datasetSentenceLabels.txt --split dev
Namespace(labels_file='/fs/clip-amr/bibinlp/blindDev/datasetSentenceLabels.txt', predictions_file='dev/datasetSentences.out', split='dev')

Correct:  [208, 105, 99]
Total:  [428, 229, 444]
Negative Acc:  0.485981308411
Neutral Acc:  0.458515283843
Positive Acc:  0.222972972973

Acc:  0.374205267938
