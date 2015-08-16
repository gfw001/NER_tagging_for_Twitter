Here is a big picture of the project’s milestone section.

1. simple_fe.py works on 
train.txt, dev.txt

e.g.
@paulwalk	O
It	O
's	O
the	O
view	O
from	O

-> train.feats, dev.feats

e.g. (both)
O	word=@paulwalk
O	word=two
O	word=weeks
O	word=.
B-facility	word=Empire
I-facility	word=State
I-facility	word=Building
O	word==
B-facility	word=ESB
O	word=.
O	word=evening
O	word=.

O	word=From
O	word=Green
O	word=Newsfeed
O	word=_COLON_
B-other	word=AHFA
O	word=extends
O	word=deadline
O	word=for
B-other	word=Sage
I-other	word=Award
O	word=5
O	word=http_COLON_//tinyurl.com/24agj38

2. crfsuite learn -m my model train.feats -> mymodel
3. crfsuite tag -m mymodel dev.feats -> pretags

e.g.
O
O
O
O
O
O
O
O
O
O
O
O
O
O
O
O
O

O
O
O

4. evaluate protégés against the gold standard tags of the devset.
python tageval.py dev.txt pretags
-> Span-level NER evaluation
   F = 0.0362,  Prec = 0.7500 (12/16),  Rec = 0.0185 (12/647)
   (1000 sentences, 19378 tokens, 647 gold spans, 16 predicted spans)
“””
“””
DATA SHAPE CHANGES IN evaluate_taggings 
e.g.
spans = convert_bio_to_spans(["B","I","B"])
-> spans==[("",0,2), ("",2,3)]
“””
def evaluate_taggings(goldseq_predseq_pairs, ignore_labels=False):
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
    print "({num_sent} sentences, {num_tokens} tokens, {num_goldspans} gold spans, {num_predspans} predicted spans)".format(**locals())

“””
OUTPUTS OF convert_bio_to_spans(bio_sequence)
“””

def test_bio_conversion():
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
    assert spans==[("a",0,1), ("b",1,2)]