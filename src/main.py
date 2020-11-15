from flask import Flask, render_template, request
import os
from docs_processing import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath('static/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST','GET'])
def search():
    input_id = 0
    query = request.form['query']
    if not query:
        return render_template('index.html')
    
    uploaded_file = request.files.getlist('file')
    
    empty_files = False
    if 'file' not in request.files:
        empty_files = True
    
    if not (empty_files):    
        for file in uploaded_file:
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        database = get_txt()
        titles = title_txt()
        df = get_DataFrame(database)
        sim_sorted = get_similiar(query, df, database)
        input_id = 1
        doc_url = titles

    else:    
        database = retrieve_docs()
        titles = get_title()
        df = get_DataFrame(database)
        sim_sorted = get_similiar(query, df, database)
        input_id = 2
        r = requests.get('https://thejakartapost.com/seasia')

        soup = BeautifulSoup(r.content, 'html.parser')
        link = []

        idx = 0
        for i in soup.find('div', {'class':'col-md-12 col-xs-12 channelLatest channelPage'}).find_all('a'):
            i['href'] = i['href'] + '?page=all'
            if ( not(is_link_double(link,i['href'],idx))  and (i['href'] != 'https://www.thejakartapost.com/seasia?page=all') and (i['href'] != 'https://www.thejakartapost.com/seasia/index?page=all') ):
                idx += 1
                link.append(i['href'])
        doc_url=link

    arrTitles = []
    arrDesc = []
    arrWordCount = []
    arrCosSim = []

    for k, v in sim_sorted:
        if v != 0.0:
            s = database[k]
            arrTitles.append(titles[k])
            arrDesc.append(s[0:s.find('.')])
            arrWordCount.append(len(s.split()))
            arrCosSim.append(v*100)
    return render_template('result.html',UPLOAD_FOLDER=UPLOAD_FOLDER, input_id=input_id, query=query, titles=arrTitles, doc_url=doc_url, desc=arrDesc, word_count=arrWordCount, cos_sim=arrCosSim)


@app.route('/upload',methods=['POST'])
def upload():
    return render_template('result.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)