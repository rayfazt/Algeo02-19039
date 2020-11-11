import re
import string
import requests
from bs4 import BeautifulSoup

def retrieve_and_clean_docs():
    # Get News Link
    r = requests.get('https://www.thejakartapost.com/seasia')

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
    count = 0
    for i in link:
      r = requests.get(i)
      soup = BeautifulSoup(r.content, 'html.parser')

      sen = []
      for i in soup.find('div', {'class':'col-md-10 col-xs-12 detailNews'}).find_all('p'):
          sen.append(i.text)
      documents.append(' '.join(sen))

    # Clean Paragraphs
    documents_clean = []
    for d in documents:
      document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
      document_test = re.sub(r'@\w+', '', document_test)
      document_test = document_test.lower()
      document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
      document_test = re.sub(r'[0-9]', '', document_test)
      document_test = re.sub(r'\s{2,}', ' ', document_test)
      documents_clean.append(document_test)
    print(documents_clean)
    return documents_clean

def is_link_double(list,filename,idx):
    if (idx == 0):
        return False
    else:
        return (filename == list[idx-1])
