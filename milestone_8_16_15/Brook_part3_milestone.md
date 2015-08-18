# Project milestone

## Run the starter code

* Given train and dev sets, plain text files, [`train.txt`] (https://github.com/aritter/twitter_nlp) and [`dev.txt`] (https://github.com/aritter/twitter_nlp).
  + __Sample__ (`train.txt`, `dev.txt`)
  <pre><code>Empire	B
  State	I
  Building	I
  =	O
  ESB	B
  .	O</code></pre>
  + part-of-speech tags
  <pre><code>NP stands for a noun phrase, VP for a verb phrase, and PP for a prepositional phrase.</code></pre>
  + IOB2 notation
  To represent a chunk (a span of tokens) with labels. Take a chunk NP as example.
  <pre><code>(B-NP) represent "a begin of a chunk".
  (I-NP) represent "an inside of a chunk".
  (O) represent "Tokens that do not belong to a chunk".</code></pre> 

* Features generation based on CRFsuite format. 
  + Extract features for both the train and dev sets. 
  + `simple_fe.py` used at this step, a simple feature extractor designed to be used with CRFsuite.
  + `train.feats` and `dev.feats` created at this step.
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

* Evaluation
  + Evaluate the pretags against the gold standard tags of the devset using `python tageval.py dev.txt predtags`
  + `tageval.py` used at this step, the evaluation script.
  + __Outputs__
    <pre><code>Span-level NER evaluation
    F = 0.0362,  Prec = 0.7500 (12/16),  Rec = 0.0185 (12/647)
    (1000 sentences, 19378 tokens, 647 gold spans, 16 predicted spans)</code></pre>
    - __In current research, system typically get F-scores in the 0.6 range.__
  + Convertion from B/I/O to spans.
    - Our evaluation works at the __span__ level.
    - `convert_bio_to_spans()` and `test_bio_conversion()` used at this step.
    - Code (label, startindex, endindex)
    <pre><code>def test_bio_conversion():
            spans = convert_bio_to_spans(["B"])
            assert spans==[("",0,1)]
            spans = convert_bio_to_spans(["B","I"])
            assert spans==[("",0,2)]
            spans = convert_bio_to_spans(["B","I","O"])
            assert spans==[("",0,2)]
            spans = convert_bio_to_spans(["O","B","I","O","O"])
            assert spans==[("",1,3)]
            spans = convert_bio_to_spans(["B","B"])
            assert spans==[("",0,1), ("",1,2)]
            spans = convert_bio_to_spans(["B","I","B"])
            assert spans==[("",0,2), ("",2,3)]
            spans = convert_bio_to_spans(["B-asdf","I-asdf","B"])
            assert spans==[("asdf",0,2), ("",2,3)]
            spans = convert_bio_to_spans(["B-asdf","I-difftype","B"])
            assert spans==[("asdf",0,1), ("difftype",1,2), ("",2,3)]
            spans = convert_bio_to_spans(["I","I"])
            assert spans==[("",0,2)]
            spans = convert_bio_to_spans(["B-a","I-b"])
            assert spans==[("a",0,1), ("b",1,2)]</code></pre>
    - __Sample__
    <pre><code>spans == [("",0,3), ("",4,5)]</code></pre>

  + __F-score__
    - Formula
      * false positive (fp) is where the tagger predicted a name, but there actually is no name in the gold standard.
      * false negative (fn) is where the gold standard has a name, but your tagger did not predict a name.
      * Precision is the ratio of true positives (tp) to all predicted positives (tp + fp).
      * Recall is the ratio of true positives (tp) to all actual positives (tp + fn).
    <pre><code>prec = tp / (tp + fp) = 1 - fp / (tp + fp)
    rec = tp / (tp + fn) = 1 - fn / (tp + fn)
    f = 2 * prec * rec / (prec + rec)</code></pre>
    

