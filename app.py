from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def welcome_page():
    return render_template('welcome_page.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'pdfFile' not in request.files:
            return redirect(url_for('upload_page', result='No file part'))
        file = request.files['pdfFile']
        if file.filename == '':
            return redirect(url_for('upload_page', result='No selected file'))
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result = analyze_pdf(filepath)
            return redirect(url_for('upload_page', result=result))
    result = request.args.get('result')
    return render_template('upload.html', result=result)

def analyze_pdf(filepath):
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
    return f'The PDF has {num_pages} pages.'

if __name__ == '__main__':
    app.run(debug=True)
