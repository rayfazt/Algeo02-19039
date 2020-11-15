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

# FOR WEBSITE IMPLEMENTATION PURPOSE, SEARCH ENGINE
import numpy as np
import pandas as pd
from tfidf import *
from vectors import *

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

def get_similar_articles(database,title):
  documents = clean_docs(database)
  filtered_documents = remove_stop_words(documents)
  stemmed_documents = stemming(filtered_documents)

  # Making dataframe from stemmed_docs
  df1 = pd.DataFrame(tfidf(stemmed_documents))
  df1 = df1.reindex(sorted(df1.columns), axis=1)
  df1 = df1.T

  # Add The Query
  q = input('Enter search query: ')
  # Convert the query to a vector
  q_tfidf = tfidf2(q, stemmed_documents)
  # Change to Dataframe for Sorting
  qdf = pd.DataFrame(list(q_tfidf.items()),columns = ['word','values'])
  qdf = qdf.sort_values(by = ['word'], ascending=True)
  # Vector of query is the elements of 'values' column
  q_vec = qdf['values'].tolist()
  sim = {}
  # Calculate the similarity
  for i in range(len(stemmed_documents)):
    sim[i] = dot_product(df1.loc[:, i].values, q_vec) / (norm(df1.loc[:, i]) * norm(q_vec))
    
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

'''
database = retrieve_docs()
titles = get_title()
# Call the function
get_similar_articles(database, titles)
'''