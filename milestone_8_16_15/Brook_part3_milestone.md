# Project milestone

## Run the starter code

* Given train and dev sets, plain text files, train.txt and dev.txt.
  + Sample
  <pre><code>Empire	B
  State	I
  Building	I
  =	O
  ESB	B
  .	O</code></pre>
  + part-of-speech tags
  NP stands for a noun phrase, VP for a verb phrase, and PP for a prepositional phrase.
  + IOB2 notation
  To represent a chunk (a span of tokens) with labels. Take a chunk NP as example.
  <pre><code>(B-NP) represent "a begin of a chunk".
  (I-NP) represent "an inside of a chunk".
  (O) represent "Tokens that do not belong to a chunk".</code></pre> 
