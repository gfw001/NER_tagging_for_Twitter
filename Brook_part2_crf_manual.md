# Brook part2: CRFsuite Documentation

Quote from [CRFsuite manual] (http://www.chokkan.org/software/crfsuite/manual.html) to help me learn about rules of CRFsuite.

1. [Format of training/tagging data] (http://www.chokkan.org/software/crfsuite/manual.html#id532502)

    `simple_fe.py` works on it.
    <pre><code>def clean_str(s):
    """Clean a word string so it doesn't contain special crfsuite characters"""
    return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")</code></pre>
