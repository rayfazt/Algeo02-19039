import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from docs_processing import clean_docs, remove_stop_words, stemming, get_similar_articles

def get_txt():
    docs = []
    for file in Path('txt').rglob('*.txt'):
        docs.append(file.parent/file.name)
    #return docs

    all_docs = []
    for doc in docs:
        with open(doc) as f:
            sen = f.read()
        all_docs.append(sen)
    
    return all_docs

def title_txt():
    titles = [os.path.splitext('*.txt')[0] for filename in os.listdir('txt')]
    return titles

print(title_txt())
'''
txt = get_txt()
title = title_txt()
# Call the function
get_similar_articles(txt, title)
'''
