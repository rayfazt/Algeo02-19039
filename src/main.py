from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    results = []
    return render_template('index.html',results=results)

@app.route('/search',methods=['POST'])
def search():
    if request.method == 'POST':
        form_data = request.form
        results = []
    return render_template('index.html',results=results)

@app.route('/upload')
def upload():
    message = ''
    args = request.args
    if 'message' in args:
        message = args.get('message')
    
    return render_template('upload.html',message=message)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)