# app.py
import os
from flask import Flask, render_template, request
from generate_caption import generate_caption
from PIL import Image

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file:
        image_path = os.path.join('static', 'uploads', file.filename)
        file.save(image_path)
        image = Image.open(image_path)
        predicted_caption = generate_caption(file.filename)

        return render_template('index.html', image_path=image_path, predicted_caption=predicted_caption)

if __name__ == '__main__':
    app.run(debug=False)
