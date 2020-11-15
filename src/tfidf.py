import pandas as pd
import math

def tf(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def idf(listDocument):
    idfDict = {}
    N = len(listDocument)

    idfDict = dict.fromkeys(listDocument[0].keys(), 0)
    for doc in listDocument:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
        
    return idfDict

def tfidf(documents):
    # documents adalah file yang sudah di preprocessing
    # stemmed documents
    total = []
    for i in range(len(documents)):
        total = set(total).union(set(documents[i]))

    wordDict_list = []
    for i in range(len(documents)):
        wordDict = dict.fromkeys(total,0)
        for word in documents[i]:
            wordDict[word] += 1
        wordDict_list.append(wordDict)

    tf_list = []
    for i in range(len(documents)):
        TF = tf(wordDict_list[i], documents[i])
        tf_list.append(TF)
    
    idfs = idf(wordDict_list)

    tfidf_list = []
    for i in range(len(documents)):
        tfidf = {}
        for word, val in tf_list[i].items():
            tfidf[word] = val*idfs[word]
        
        tfidf_list.append(tfidf)
    
    return tfidf_list

def tfidf2(query, documents):
    q_words = query.split(" ")
    q_total = set(q_words)
    
    total = []
    for i in range(len(documents)):
        total = set(total).union(set(documents[i]))

    wordDict_list = []
    for i in range(len(documents)):
        wordDict = dict.fromkeys(total,0)
        for word in documents[i]:
            wordDict[word] += 1
        wordDict_list.append(wordDict)

    # Count Vector
    wordDict = dict.fromkeys(total, 0)
    for word in q_words:
        error = False
        try:
            wordDict[word] += 1
        except KeyError:
            error = True
    
    tfs = tf(wordDict, q_words)
    idfs = idf(wordDict_list)

    tfidf = {}
    for word, val in tfs.items():
        tfidf[word] = val*idfs[word]
    
    return tfidf