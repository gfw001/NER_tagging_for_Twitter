# Brook part2: CRFsuite Documentation

Quote from [CRFsuite manual] (http://www.chokkan.org/software/crfsuite/manual.html) to help me learn about rules of CRFsuite.

<pre><code>def clean_str(s):
    """Clean a word string so it doesn't contain special crfsuite characters"""
    return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")</code></pre>
