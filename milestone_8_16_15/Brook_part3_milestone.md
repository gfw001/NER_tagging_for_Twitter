# Project milestone

## Run the starter code

* Given train and dev sets, plain text files, `train.txt` and `dev.txt`.
  + __Sample__ (`train.txt`, `dev.txt`)
  <pre><code>Empire	B
  State	I
  Building	I
  =	O
  ESB	B
  .	O</code></pre>
  + part-of-speech tags
  <pre><code>NP stands for a noun phrase, VP for a verb phrase, and PP for a prepositional phrase.</code></pre>
  || NP || a noun phrase || 
  + IOB2 notation
  To represent a chunk (a span of tokens) with labels. Take a chunk NP as example.
  <pre><code>(B-NP) represent "a begin of a chunk".
  (I-NP) represent "an inside of a chunk".
  (O) represent "Tokens that do not belong to a chunk".</code></pre> 

* Features generation based on CRFsuite format. 
  + Extract features using `simple_fe.py` for both the train and dev sets. `train.feats` and `dev.feats` created at this step.
  + __Sample__ (`train.feats`, `dev.feats`)
  <pre><code>B word=Empire
  I	word=State
  I	word=Building
  O	word==
  B	word=ESB
  O	word=.</code></pre>

* Training
  + Train a model on the training set `train.feats` using `crfsuite learn -m mymodel train.feats`.
  + `mymodel` created at this step.
  + It should take less than a minute to train. (it may converge after 86 iterations of __LBFGS__.)

* Tagging
  + Make predictions on the devset, using the model you just trained. Command-line `crfsuite tag -m mymodel dev.feats > predtags`. `pretags` created at this step.
  + __Sample__ (`pretags`)
  <pre><code>B
  I
  I
  O
  B
  O</code></pre>
