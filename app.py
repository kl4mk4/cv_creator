from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ścieżka do zapisywania danych i przesłanych zdjęć
DATA_FILE = 'data.json'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/save', methods=['POST'])
def save():
    data = request.form.to_dict()
    if 'photo' in request.files:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            data['photo'] = url_for('static', filename='uploads/' + filename)
    save_data(data)
    return render_template('preview.html', data=data)

@app.route('/view_cv')
def view_cv():
    data = load_data()
    return render_template('cv_template.html', data=data)

@app.route('/set_language/<lang>')
def set_language(lang):
    data = load_data()
    data['language'] = lang
    save_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
