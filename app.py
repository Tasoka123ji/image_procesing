import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads/'
PROCESSED_FOLDER = 'static/processed/'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Process the image using OpenCV
            processed_filepath = process_image(filepath, file.filename)
            
            return render_template('index.html', original_image=filepath, processed_image=processed_filepath)

    return render_template('index.html')

def process_image(filepath, filename):
    # Read the image using OpenCV
    image = cv2.imread(filepath)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Save the processed image to the processed folder
    processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], f"processed_{filename}")
    cv2.imwrite(processed_filepath, gray_image)
    
    return processed_filepath

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

