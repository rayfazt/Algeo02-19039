from flask import Flask, render_template, request
import os
from docs_processing import get_similar_articles
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
    uploaded_file= request.files.getlist('file')
    for file in uploaded_file:
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    
    titles =['uzumaki bayu','uzumaki saburo']
    doc_url=['kipli.txt','kipli2.txt']
    desc=['ini isinya kalimat pertama','ini isinya kalimat kedua']
    word_count=['203','102']
    cos_sim=['0.709123','0.02312']
    return render_template('result.html', query=query, titles=titles, doc_url=doc_url, desc=desc, word_count=word_count, cos_sim=cos_sim)


@app.route('/upload',methods=['POST'])
def upload():
    return render_template('result.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)