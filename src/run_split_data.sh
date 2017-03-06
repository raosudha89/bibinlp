#!/bin/bash

#PBS -S /bin/sh
#PBS -N bibinlp
#PBS -l pmem=32g
#PBS -m abe
#PBS -l walltime=48:00:00

SCRIPTS_DIR=/fs/clip-amr/bibinlp/src
DATA_DIR=/fs/clip-amr/bibinlp/stanfordSentimentTreebank
OUTPUT_DIR=/fs/clip-amr/bibinlp

python $SCRIPTS_DIR/split_data.py   $DATA_DIR/datasetSentences.txt \
                                    $DATA_DIR/datasetSplit.txt \
                                    $DATA_DIR/sentiment_labels.txt \
                                    $DATA_DIR/dictionary.txt \
                                    $OUTPUT_DIR/train \
                                    $OUTPUT_DIR/dev \
                                    $OUTPUT_DIR/test
