# Brook part2: CRFsuite Documentation

##Quote from [CRFsuite manual] (http://www.chokkan.org/software/crfsuite/manual.html) to help me learn about rules of CRFsuite.

1. [Format of training/tagging data] (http://www.chokkan.org/software/crfsuite/manual.html#id532502)

    `simple_fe.py` works on it.
    <pre><code>def clean_str(s):
        """Clean a word string so it doesn't contain special crfsuite characters"""
        return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")</code></pre>

2. [Installation] (http://www.chokkan.org/software/crfsuite/manual.html#id489766) (Linux and Windows)
    + On Mac, we found [these instructions] (http://stackoverflow.com/questions/25838517/how-to-get-crfsuite-to-work-on-mac-os-x) worked (installing using Homebrew).

3. [Usage] (http://www.chokkan.org/software/crfsuite/manual.html#id490441) 
    + [Training] (http://www.chokkan.org/software/crfsuite/manual.html#id490773)
        * Commands to train a CRF model from a training set, `crfsuite learn -m mymodel train.feats` used in this project.
        * [Graphical models] (http://www.chokkan.org/software/crfsuite/manual.html#id491135) is __1d: 1st-order Markov CRF with dyad features__
        * [Training algorithms] (http://www.chokkan.org/software/crfsuite/manual.html#id491233) is __lbfgs: Limited-memory Broyden-Fletcher-Goldfarb-Shanno (L-BFGS) method__
    + [Tagging] (http://www.chokkan.org/software/crfsuite/manual.html#id493459)
        * Commands to tag a data using a CRF model, `crfsuite tag -m mymodel dev.feats > predtags` used in this project.
    + [Model dump] (http://www.chokkan.org/software/crfsuite/manual.html#id493687)
        * To dump a CRF model in plain-text format, enter the following command, `crfsuite dump`.

