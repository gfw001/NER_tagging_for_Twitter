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
  + It should take less than a minute to train. (it converged after 86 iterations of __LBFGS__.)

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
    <pre><code>prec = tp / (tp + fp) = 1 - fp / (tp + fp)
    rec = tp / (tp + fn) = 1 - fn / (tp + fn)
    f = 2 * prec * rec / (prec + rec)</code></pre>
      * __false positive (fp)__ is where the tagger predicted a name, but there actually is no name in the gold standard.
      * __false negative (fn)__ is where the gold standard has a name, but your tagger did not predict a name.
      * __Precision__ is the ratio of __true positives (tp)__ to all predicted positives (tp + fp). Precision goes down if you make lots of false positives.
      * __Recall (sensitivity)__ is the ratio of __true positives (tp)__ to all actual positives (tp + fn).
      * __Specificity__ is the ratio of __true negative (tn)__ to (tn + fp)
    - Code
    <pre><code>def evaluate_taggings(goldseq_predseq_pairs, ignore_labels=False):
            """a list of (goldtags,predtags) pairs.  goldtags and predtags are both lists of strings, of the same length."""
            num_sent = 0
            num_tokens= 0
            num_goldspans = 0
            num_predspans = 0
            
            tp, fp, fn = 0,0,0
    
            for goldseq,predseq in goldseq_predseq_pairs:
                N = len(goldseq)
                assert N==len(predseq)
                num_sent += 1
                num_tokens += N

                if ignore_labels:
                    goldseq = kill_labels(goldseq)
                    predseq = kill_labels(predseq)
        
                goldspans = convert_bio_to_spans(goldseq)
                predspans = convert_bio_to_spans(predseq)
        
                num_goldspans += len(goldspans)
                num_predspans += len(predspans)
        
                goldspans_set = set(goldspans)
                predspans_set = set(predspans)
                
                tp += len(goldspans_set & predspans_set)
                fp += len(predspans_set - goldspans_set)
                fn += len(goldspans_set - predspans_set)
    
            prec = tp/(tp+fp) if (tp+fp)>0 else 0
            rec =  tp/(tp+fn) if (tp+fn)>0 else 0
            f1 = 2*prec*rec / (prec + rec)
            print "F = {f1:.4f},  Prec = {prec:.4f} ({tp}/{tpfp}),  Rec = {rec:.4f} ({tp}/{tpfn})".format(tpfp=tp+fp, tpfn=tp+fn, **locals())
            print "({num_sent} sentences, {num_tokens} tokens, {num_goldspans} gold spans, {num_predspans} predicted spans)".format(**locals())</code></pre>
    
## Report

* Compare the tag predictions to the gold standard
  + put them side-by-side using `paste predtags dev.txt`
  + __Sample__
  <pre><code>B	Chicago	B
  O	Weekend	O
  O	Events	O
  O	:	O
  O	Lebowski	B
  O	Fest	I
  O	,	O
  O	Dave	B
  O	Matthews	I
  O	,	O
  O	Latin	O
  O	Music	O
  O	And	O
  O	More	O
  O	:	O
  O	The	O
  O	lively	O
  O	weekend	O
  O	(	O
  O	well	O
  O	,	O
  O	Friday	O
  O	throu	O
  O	...	O
  O	http://bit.ly/cLTnyl	O</code></pre>

* Look at `mymodel` using `crfsuite dump mymodel`.
  + __Sample__
  <pre><code>FILEHEADER = {
    magic: lCRF
    size: 525968
    type: FOMC
    version: 100
    num_features: 0
    num_labels: 3
    num_attrs: 7072
    off_features: 0x30
    off_labels: 0x23618
    off_attrs: 0x23E8A
    off_labelrefs: 0x6B82C
    off_attrrefs: 0x6B878
  }

  LABELS = {
        0: O
        1: B
        2: I
  }

  ATTRIBUTES = {
        0: word=@paulwalk
        1: word=It
        2: word='s
        3: word=the
        4: word=view
        5: word=from
        6: word=where
        7: word=I
        8: word='m
        9: word=living
       10: word=for
       11: word=two
       12: word=weeks
       13: word=.
       14: word=Empire
       15: word=State
       16: word=Building
       17: word==
       18: word=ESB
       ...
  }
  
  TRANSITIONS = {
    (1) O --> O: 4.059304
    (1) O --> B: 2.451315
    (1) B --> O: 2.035927
    (1) B --> B: -0.684482
    (1) B --> I: 4.348084
    (1) I --> O: 1.354929
    (1) I --> B: -1.288914
    (1) I --> I: 3.140151
  }

  STATE_FEATURES = {
    ...
    (0) word=Soulja --> B: 0.919394
    (0) word=Boy --> O: -0.897372
    (0) word=Boy --> I: 1.065956
    (0) word=| --> O: 0.717401
    (0) word=TheDeAndreWay --> O: 0.117317
    (0) word=com --> O: 0.327298
    (0) word=DeAndre --> O: -0.344690
    (0) word=DeAndre --> I: 0.491510
    (0) word=Way --> O: -0.529700
    (0) word=Way --> I: 0.600220
    (0) word=stores --> O: 0.113670
    ...
  }</code></pre>
