from flask import Flask, render_template, request
import os
from docs_processing import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.abspath('txt/')
print(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST','GET'])
def search():
    query = request.form['query']
    if not query:
        return render_template('index.html')
    
    uploaded_file = request.files.getlist('file')
    
    empty_files = True
    if uploaded_file:
        empty_files = False
    
    if not (empty_files):    
        for file in uploaded_file:
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        database = get_txt()
        titles = title_txt()
        df = get_DataFrame(database)
        sim_sorted = get_similiar(query, df, database)

    else:    
        database = retrieve_docs()
        titles = get_title()
        df = get_DataFrame(database)
        sim_sorted = get_similiar(query, df, database)

    arrTitles = []
    arrDesc = []
    arrWordCount = []
    arrCosSim = []
    arrUrl = []
    for k, v in sim_sorted:
        if v != 0.0:
            s = database[k]
            arrTitles.append(titles[k])
            arrDesc.append(s[0:s.find('.')])
            arrWordCount.append(len(s.split()))
            arrCosSim.append(v*100)
    
    return render_template('result.html', query=query, titles=arrTitles, doc_url=arrUrl, desc=arrDesc, word_count=arrWordCount, cos_sim=arrCosSim)

@app.route('/upload',methods=['POST'])
def upload():
    return render_template('result.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)