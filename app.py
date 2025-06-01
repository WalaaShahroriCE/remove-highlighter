
from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return "لا يوجد ملف مرفق", 400

    file = request.files['image']
    if file.filename == '':
        return "لم يتم اختيار صورة", 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    # معالجة الصورة
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    cleaned = cv2.bitwise_not(mask)
    result = cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)

    cleaned_filename = 'cleaned_' + filename
    result_path = os.path.join(RESULT_FOLDER, cleaned_filename)
    cv2.imwrite(result_path, result)

    return render_template('result.html',
                           original_url=url_for('static', filename='uploads/' + filename),
                           cleaned_url=url_for('static', filename='results/cleaned_' + filename))

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)