# Brook part 1: CRFsuite Tutorial

##Quote from [CRFsuite tutorial] (http://www.chokkan.org/software/crfsuite/tutorial.html#id528076) help me to clear tasks, outputs and scripts used in this project.

1. [Feature (attribute) generation] (http://www.chokkan.org/software/crfsuite/tutorial.html#id485365)

  The most important process for machine-learning approaches is to preprocess the training and testing data to extract features that express the characteristics of words in the data, because a feature design greatly affects the labeling accuracy.

2. [Training] (http://www.chokkan.org/software/crfsuite/tutorial.html#id488968)

3. [Tagging] (http://www.chokkan.org/software/crfsuite/tutorial.html#id489402)
  
  In project, evalution section put here. (use `tageval.py` instead)
  
  When tagging, CRFsuite ignores labels in the input data or uses them for measuring the performance of predictions.

+ [Dumping the model file] (http://www.chokkan.org/software/crfsuite/tutorial.html#id489453)

+ [Notes on writing attribute extractors] (http://www.chokkan.org/software/crfsuite/tutorial.html#id489467)

  In project, we use `simple_fe.py` instead of `chunking.py`.
