# Active Learning for Rumor Identification on Social Media EMNLP2021
[Paper](https://aclanthology.org/2021.findings-emnlp.387/)

Authors: Parsa Farinneya, Mohammad Mahdi Abdollah Pour, Sardar Hamidian and Mona Diab 

## Abstract
Social media has emerged as a key channel for seeking information. Online users spend several hours reading, posting, and searching for news on microblogging platforms daily. However, this could act as a double-edged sword especially when not all information online is reliable. Moreover, the inherently unmoderated nature of social media renders identifying unverified information ever more challenging. Most of the existing approaches for rumor tracking are not scalable because of their dependency on a significant amount of labeled data. In this work, we investigate this problem from different angles. We design an Active-Transfer Learning (ATL) strategy to identify rumors with a limited amount of annotated data. We go beyond that and investigate the impact of leveraging various machine learning approaches in addition to different contextual representations. We discuss the impact of multiple classifiers on a limited amount of annotated data followed by an interactive approach to gradually update the models by adding the least certain samples (LCS) from the pool of unlabeled data. Our proposed Active Learning (AL) strategy achieves faster convergence in terms of the F-score while requiring fewer annotated samples (42% of the whole dataset for the best model).


This paper includes extensive experiments, so here we share codes to automaticly run experiments and visualize them.

## Running Experiment
Open notebook "ATL_Experiment_Runner.ipynb" and set your desired experiment by setting values of topic_num, reps, models and stratefies. For example: 
```
topic_num = 2 # 2 for Ferguson, 8 for Sydney seige and 0 for Charlie Hebdo

reps = ['tweetBERT'] # or BERT or Glove

models = ['knn3','knn5','lda','gp','qda'] # or mlp, svm, rf, Ada, LR

stratefies = ['lc','Random'] 
```
names for models, embeddings and startegies are given in [Model, Embeddings, Strategies](## Model, Embeddings, Strategies)

The run all the cells to the end. It will produce a numpy file (.np) for each experiment with this 
format:

`Embedding_Name-Model_Name-Strategy_Name-Topic_Number-metrix.np` 

such as BERT-svm-lc-8-f1.np. 
## Visualizing Results
Save all .np results in a folder name "results" then open "ATL_Visualization_and_Table_Creation.ipynb" and run the cells for tables and plots.

## Creating Embeding Files
Embeddigns are computed and saved to "vectorization" folder (used by "ATL_Experiment_Runner.ipynb"), but if you want to create from scracth you can use ATL_Create_Embedding_Files.ipynb


## Model, Embeddings, Strategies 

### Models

- "Ada" for AdaBoostClassifier()
- "svm" for svm.SVC(probability=True)
- "rf" for RandomForestClassifier(max_depth=1000, random_state=0)
- "LR" for LogisticRegression(random_state=0)
- "knn3" for  KNeighborsClassifier(n_neighbors=3)
- "knn5" for KNeighborsClassifier(n_neighbors=5)
- "gp" for GaussianProcessClassifier()
- "lda" for LinearDiscriminantAnalysis()
- "qda" for QuadraticDiscriminantAnalysis()
- "mlp" for Pytorch MLP 

### Embeddings
- "BERT" for [BERT](https://arxiv.org/abs/1810.04805)
- "tweetBERT" for [tweetBERT](https://arxiv.org/abs/2010.11091)
- "GLOVE" for [Twitter Glove](https://nlp.stanford.edu/projects/glove/)

### Strategies
- "lc"  for Least Confidence
- "Random" for Random Selection

## Cite This Paper
```
@inproceedings{farinneya2021active,
  title={Active Learning for Rumor Identification on Social Media},
  author={Farinneya, Parsa and Abdollah Pour, Mohammad Mahdi and Hamidian, Sardar and Diab, Mona},
  booktitle={Findings of the Association for Computational Linguistics: EMNLP 2021},
  pages={4556--4565},
  year={2021}
}
```