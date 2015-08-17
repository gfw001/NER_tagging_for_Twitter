# Brook part 1: CRFsuite Tutorial

Quote from [CRFsuite tutorial] (http://www.chokkan.org/software/crfsuite/tutorial.html#id528076) help me to clear tasks, outputs and scripts used in this project.

1. [Feature (attribute) generation] (http://www.chokkan.org/software/crfsuite/tutorial.html#id485365)

2. [Training] (http://www.chokkan.org/software/crfsuite/tutorial.html#id488968)

3. [Tagging] (http://www.chokkan.org/software/crfsuite/tutorial.html#id489402)
In project, evalution section put here. (use `tageval.py` instead)

Apply the CRF model and tag chunk labels to the test data.
Even though the test data has chunk labels annotated (for evaluation purposes), CRFsuite ignores the existing labels and outputs label sequences (one label per line) predicted by the model.

4. [Dumping the model file] (http://www.chokkan.org/software/crfsuite/tutorial.html#id489453)

5. [Notes on writing attribute extractors] (http://www.chokkan.org/software/crfsuite/tutorial.html#id489467)
In project, we use `simple_fe.py` instead of `chunking.py`.
