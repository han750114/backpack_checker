from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
from detect_items import process_and_detect

UPLOAD_FOLDER = 'static/uploaded'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            detected_items, missing_items = process_and_detect(filepath)
            result = {
                'detected': detected_items,
                'missing': missing_items,
                'filename': file.filename
            }
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
