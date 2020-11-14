# Modules for Retrieving Files from Web
import re
import string
import requests
from bs4 import BeautifulSoup

# Modules for removing stop words and stemming
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def is_link_double(list,filename,idx):
    if (idx == 0):
        return False
    else:
        return (filename == list[idx-1])

def retrieve_docs():
    # Get News Link
    r = requests.get('https://thejakartapost.com/seasia')

    soup = BeautifulSoup(r.content, 'html.parser')
    link = []

    idx = 0
    for i in soup.find('div', {'class':'col-md-12 col-xs-12 channelLatest channelPage'}).find_all('a'):
      i['href'] = i['href'] + '?page=all'
      if ( not(is_link_double(link,i['href'],idx))  and (i['href'] != 'https://www.thejakartapost.com/seasia?page=all') and (i['href'] != 'https://www.thejakartapost.com/seasia/index?page=all') ):
        idx += 1
        link.append(i['href'])
    
    # Retrieve Paragraph
    documents=[]
    for i in link:
      r = requests.get(i)
      soup = BeautifulSoup(r.content, 'html.parser')

      sen = []
      for i in soup.find('div', {'class':'col-md-10 col-xs-12 detailNews'}).find_all('p'):
          sen.append(i.text)
      documents.append(' '.join(sen))
    
    return documents

def get_title():
    # Get News Link
    r = requests.get('https://thejakartapost.com/seasia')

    soup = BeautifulSoup(r.content, 'html.parser')
    link = []

    idx = 0
    for i in soup.find('div', {'class':'col-md-12 col-xs-12 channelLatest channelPage'}).find_all('a'):
      i['href'] = i['href'] + '?page=all'
      if ( not(is_link_double(link,i['href'],idx))  and (i['href'] != 'https://www.thejakartapost.com/seasia?page=all') and (i['href'] != 'https://www.thejakartapost.com/seasia/index?page=all') ):
        idx += 1
        link.append(i['href'])

    #Retrieve Title
    titles=[]
    for i in link:
      r = requests.get(i)
      soup = BeautifulSoup(r.content, 'html.parser')
      for i in soup.find('div', {'class':'col-xs-12 areaTitle'}).find_all('h1'):
          titles.append(i.text)

    return titles

def clean_docs(documents):
    documents_clean = []
    for d in documents:
      document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
      document_test = re.sub(r'@\w+', '', document_test)
      document_test = document_test.lower()
      document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
      document_test = re.sub(r'[0-9]', '', document_test)
      document_test = re.sub(r'\s{2,}', ' ', document_test)
      documents_clean.append(document_test)
    
    return documents_clean

def remove_stop_words(documents):
  # Removing Stop Words
  stop_words = set(stopwords.words('english'))
  ps = PorterStemmer()

  filtered_documents = []
  for i in range(len(documents)):
    word_tokens = word_tokenize(documents[i])  
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []

    for w in word_tokens: 
      if w not in stop_words: 
        filtered_sentence.append(w)
    
    filtered_documents.append(filtered_sentence)
  
  return filtered_documents

def stemming(documents):
  ps = PorterStemmer()
  stemmed_documents = []
  for i in range(len(documents)):
    words = documents[i]
    temp_array = []
    for w in words:
      w = ps.stem(w)
      temp_array.append(w)

    stemmed_documents.append(temp_array)
  return stemmed_documents

# DATA PRE-PROCESSING
database = retrieve_docs()
title = get_title()
documents = clean_docs(database)
filtered_documents = remove_stop_words(documents)
stemmed_documents = stemming(filtered_documents)

# FOR WEBSITE IMPLEMENTATION PURPOSE, SEARCH ENGINE
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

def get_similar_articles(q, df, database,title):
  # Convert the query to a vector
  q = [q]
  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
  sim = {}
  # Calculate the similarity
  for i in range(10):
    sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
  # Sort the values 
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
  # Print the articles and their similarity values
  cnt = 0
  for k, v in sim_sorted:
    if v != 0.0:
      s = database[k]
      print(title[k])
      print("Jumlah Kata:", len(s.split()))  
      print("Tingkat Kemiripan:", v*100, '%')
      print(s[0:s.find('.')])
      print()
      cnt += 1
  if cnt == 0:
      print("No matching results found")

docs = [] # Setelah di pre-procces digabung jadi satu sentence
for i in range(len(documents)):
  docs.append(' '.join(stemmed_documents[i]))

# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()
# It fits the data and transform it as a vector
X = vectorizer.fit_transform(docs)
# Convert the X as transposed matrix
X = X.T.toarray()
# Create a DataFrame and set the vocabulary as the index
df = pd.DataFrame(X, index=vectorizer.get_feature_names())

# Add The Query
q1 = input('Enter search query: ')
# Call the function
get_similar_articles(q1, df, database, title)
