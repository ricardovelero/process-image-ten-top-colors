from flask import Flask, render_template, request
import numpy as np
from PIL import Image


app = Flask(__name__)

# Set the path where uploaded images will be stored
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def process_image(image_path):
    # Load the image using NumPy
    image = np.array(Image.open(image_path))

    # Reshape the image array to a 2D array of pixels
    pixels = image.reshape(-1, 3)

    # Count the occurrence of each unique color in the image
    color_counts = np.unique(pixels, axis=0, return_counts=True)

    # Sort the colors based on their occurrence
    sorted_colors = sorted(
        zip(color_counts[0], color_counts[1]), key=lambda x: x[1], reverse=True)

    # Get the top 10 most used colors
    top_colors = sorted_colors[:10]

    return top_colors


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded in the request
    if 'file' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return 'No selected file.', 400

    # Save the uploaded file to the upload folder
    file_path = app.config['UPLOAD_FOLDER'] + '/' + file.filename
    file.save(file_path)

    # Process the uploaded image to find the top colors
    top_colors = process_image(file_path)

    return render_template('result.html', colors=top_colors, image_filename=file.filename)


if __name__ == '__main__':
    app.run(debug=True)
