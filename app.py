from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from detect_item import process_and_detect_b

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploaded'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    found, missing, crop_results, filename = [], [], [], None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            found, missing, crop_results, filename = process_and_detect_b(filepath)

    return render_template('index.html', found=found, missing=missing, crop_results=crop_results, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)