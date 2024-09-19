import os
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from models.style_transfer import style_transfer
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/style-transfer', methods=['POST'])
def transfer_style():
    if 'content' not in request.files or 'style' not in request.files:
        return jsonify({"error": "Missing content or style image"}), 400

    content_file = request.files['content']
    style_file = request.files['style']

    if content_file.filename == '' or style_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not (allowed_file(content_file.filename) and allowed_file(style_file.filename)):
        return jsonify({"error": "Invalid file format. Use JPEG, PNG, GIF, or BMP"}), 400

    content_path = 'temp_content.jpg'
    style_path = 'temp_style.jpg'

    content_file.save(content_path)
    style_file.save(style_path)

    try:
        stylized_image = style_transfer(content_path, style_path)

        img = Image.fromarray((stylized_image[0] * 255).astype(np.uint8))

        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)

        return send_file(byte_io, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(content_path):
            os.remove(content_path)
        if os.path.exists(style_path):
            os.remove(style_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))