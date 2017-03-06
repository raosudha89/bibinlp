=== DATA SOURCE ===
This is the dataset of the paper:
Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank
Richard Socher, Alex Perelygin, Jean Wu, Jason Chuang, Christopher Manning, Andrew Ng and Christopher Potts
Conference on Empirical Methods in Natural Language Processing (EMNLP 2013)

Each sentence in this dataset corresponds to a review from a pool of Rotten Tomatoes reviews. Please read the paper for details on extracting a sentence from a review
Each sentence is given a sentiment label (negative, neural or positive)
Each sentence has been parsed into a parse tree & and each of its phrases has been given a sentiment label (negative, neural or positive)
We provide the phrase level sentiment labels for the training data (which you are free to use or ignore)

=== DATA FORMAT ===

The three folders correspond to:
1. train includes two files in TSV (tab separated values) format:
	a. datasetSentences contains sentence IDs, sentences, sentiment labels and positivity probabiltites separated by tabs 
	b. datasetPhrases contains phrase IDs, phrases, sentiment labels and positivity probabilites separated by tabs
   Please note that phrase ids and sentence ids are not the same. A phrase can be a part of multiple sentences

2. dev includes one file in TSV (tab separated values) format:
	a. datasetSentences contains sentence IDs and sentences separated by tabs 

3. test includes one file in TSV (tab separated values) format:
	a. datasetSentences contains sentence IDs and sentences separated by tabs 

=== SENTIMENT LABELS ===

There are three classes of sentiment labels: -1, 0, +1 corresponding to negative, neutral, positive, respectively
Each sentence in the training data is also associated with a positivity probability which is a number between 0 and 1
You can recover the 3 classes by mapping the positivity probability using the following cut-offs:
[0, 0.4], (0.4, 0.6), [0.6, 1.0] 
