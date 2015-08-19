from pylab import *
plt.rc('figure', figsize=(8, 5))
import pprint
import string
import json
import urllib
import nlpk
sys.path.append('/Users/Eamon___/Documents/workspace/tweetTagging/src/MyTagging/ark-tweet-nlp-0.3.2')
import CMUTweetTagger

api_key = 'AIzaSyD2cs-8bR-hdVd5pVddJ8wEKztdS6tR3Rc'
filters = '(any type:/people/person)'
service_url = 'https://www.googleapis.com/freebase/v1/search'

def read_natianalFile(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]
    
    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """
    wordSet = set()
    lines = open(filename).read().strip().split("\n")
    ret = []
    for line in lines:
        sent = line.split("|")[1].split(" ")
        for word in sent:
            wordSet.add(word)
        
    return wordSet

def read_freebase(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]
    
    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """
    wordSet = set()
    lines = open(filename).read().strip().split("\n")
    ret = []
    for line in lines:
        sent = line.split("\t")
        words = sent[1][1:-4].split(" ")
        for word in words:
            wordSet.add(word)
        
    return wordSet



def read_file(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]
    
    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """
    sentences = open(filename).read().strip().split("\n\n")
    ret = []
    for sent in sentences:
        lines = sent.split("\n")
        pairs = [L.split("\t") for L in lines]
        tokens = [tok for tok,tag in pairs]
        newTokens = []
        for i in range(len(tokens)):
            w = clean_str(tokens[i])
            newTokens.append(w)

        """
        mySentence = " ".join(newTokens)
        myList = []
        myList.append(mySentence)
        tagForWord = CMUTweetTagger.runtagger_parse(myList, run_tagger_cmd="java -XX:ParallelGCThreads=2 -Xmx500m -jar /Users/chenxiao/Documents/NatureLanguageProcessing/starter_code/ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar")
        """
        tags = [tag for tok,tag in pairs]
        ret.append( (newTokens,tags) )
    return ret

def clean_str(s):
    """Clean a word string so it doesn't contain special crfsuite characters"""
    return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")

def extract_features_for_sentence1(tokens):
    N = len(tokens)
    feats_per_position = [set() for i in range(N)]
    for t in range(N):
        w = clean_str(tokens[t])
        feats_per_position[t].add("word=%s" % w)
    return feats_per_position

def extract_features_for_sentence(pairs):
    N = len(pairs[0])
    feats_per_position = []
    tagSet = nltk.pos_tag(pairs[0])
    for t in range(N):  	
    	newList = []
        newList.append("word[0]=%s" % pairs[0][t].lower() +":2")
        count = 1
        while(t-count >= 0 and count < 3):
            #newList.append("tag[%d]=%s" % (0-count, tagSet[t-count][1]))
            newList.append("word[%d]=%s" % (0-count, pairs[0][t-count].lower()))
            count += 1
        count = 1
        while(t+count < N and count < 3):
            #newList.append("tag[%d]=%s" % (0+count, tagSet[t+count][1]))
            newList.append("word[%d]=%s" % (0+count, pairs[0][t+count].lower()))
            count += 1
        if(t == 0):
            newList.append("__BOS__")
        if(t == N-1):
            newList.append("__EOS__")

        if(len(pairs[0][t]) >= 3):
            newList.append("character[0]=%s" % pairs[0][t][0])
            newList.append("character[1]=%s%s" % (pairs[0][t][0],pairs[0][t][1]))
            newList.append("character[2]=%s%s%s" % (pairs[0][t][0],pairs[0][t][1],pairs[0][t][2]))
            newList.append("character[-1]=%s" % pairs[0][t][-1])
            newList.append("character[-2]=%s%s" % (pairs[0][t][-2],pairs[0][t][-1]))
            newList.append("character[-3]=%s%s%s" % (pairs[0][t][-2],pairs[0][t][-1],pairs[0][t][-3]))
        elif(len(pairs[0][t]) == 2):
            newList.append("character[0]=%s" % pairs[0][t][0])
            newList.append("character[1]=%s%s" % (pairs[0][t][0],pairs[0][t][1]))
            newList.append("character[-1]=%s" % pairs[0][t][-1])
            newList.append("character[-2]=%s%s" % (pairs[0][t][-2],pairs[0][t][-1]))
        elif(len(pairs[0][t]) == 1):
            newList.append("character[0]=%s" % pairs[0][t][0])
            newList.append("character[-1]=%s" % pairs[0][t][-1])
        
        newList.append("shape_feature=%s" % shape_features(pairs[0][t]))

        if(pairs[0][t][0].isupper()):
            newList.append("start_with_upper")
        elif(pairs[0][t][0].islower()):
            newList.append("start_with_lower")
        else:
            newList.append("start_with_other")

        
        if(pairs[0][t] in freebaseSet):
            newList.append("freebase entity")

        if(pairs[0][t] in nationalSet):
            newList.append("national entity")
        else:
            newList.append("not_national entity")

        #newList.append("tag is %s" % pairs[2][t][1])
        #print pairs[2][t][1]
        feats_per_position.append(newList)
    return feats_per_position


def extract_features_for_file(input_file, output_file):
    """This runs the feature extra ctor on input_file, and saves the output to
    output_file."""
    sents = read_file(input_file)
    with open(output_file,'w') as output_fileobj:
        for i in range(len(sents)):
            feats = extract_features_for_sentence(sents[i])
            for t in range(len(feats)):
                feats_tabsep = "\t".join(feats[t])
                print>>output_fileobj, "%s\t%s" % (sents[i][1][t], feats_tabsep)
            print>>output_fileobj, ""

def shape_features(word):
    s = ""
    if(word[0].isupper()):
        s = "A"
    elif(word[0].islower()):
        s = "a"
    else:
        s = "!"
    for i in range(1, len(word)):
        if(word[i].isupper() and s[-1] != "A"):
            s += "A"
        elif(word[i].islower() and s[-1] != "a"):
            s += "a"
        elif(not word[i].isupper() and s[-1] != "!"):
            s += "!"
    return s


nationalSet = read_natianalFile("NationalFile.txt")
freebaseSet = read_freebase("entity.txt")
extract_features_for_file("train.txt", "train.feats")
extract_features_for_file("dev.txt", "dev.feats")