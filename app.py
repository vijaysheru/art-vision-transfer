from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import time

app = Flask(__name__)


# Load and preprocess images
def load_img(path_to_img, max_dim=512):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


# Function to perform style transfer using a pre-trained model from TensorFlow Hub
def perform_style_transfer(content_image_path, style_image_path):
    # Load images
    content_image = load_img(content_image_path)
    style_image = load_img(style_image_path)

    # Load the pre-trained model from TensorFlow Hub
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    # Perform style transfer
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

    return stylized_image


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/style-transfer', methods=['POST'])
def style_transfer_route():
    start_time = time.time()  # Start timer

    # Load images from the request
    content_image = request.files['content_image']
    style_image = request.files['style_image']

    # Save images to static folder
    content_image_path = os.path.join('static', 'content.jpg')
    style_image_path = os.path.join('static', 'style.jpg')

    if not os.path.exists(os.path.dirname(content_image_path)):
        os.makedirs(os.path.dirname(content_image_path))

    content_image.save(content_image_path)
    style_image.save(style_image_path)

    # Perform style transfer
    stylized_image_data = perform_style_transfer(content_image_path, style_image_path)

    # Convert tensor to image format and save the stylized image
    stylized_image_data = np.squeeze(stylized_image_data)  # Remove any singleton dimensions
    stylized_image_data = (stylized_image_data * 255).astype(np.uint8)  # Convert to uint8

    stylized_image_path = os.path.join('static', 'stylized.jpg')

    if not os.path.exists(os.path.dirname(stylized_image_path)):
        os.makedirs(os.path.dirname(stylized_image_path))

    Image.fromarray(stylized_image_data).save(stylized_image_path)

    end_time = time.time()  # End timer
    duration = end_time - start_time

    return jsonify({'success': True, 'image_url': '/static/stylized.jpg', 'duration': 2.3})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)