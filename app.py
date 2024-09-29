import os
import io
import boto3
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from models.style_transfer import style_transfer
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
s3_client = boto3.client('s3')

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

    try:
        # Save files to S3
        content_key = f"temp_content_{content_file.filename}"
        style_key = f"temp_style_{style_file.filename}"

        s3_client.upload_fileobj(content_file, S3_BUCKET, content_key)
        s3_client.upload_fileobj(style_file, S3_BUCKET, style_key)

        # Get S3 URLs
        content_url = s3_client.generate_presigned_url('get_object',
                                                       Params={'Bucket': S3_BUCKET, 'Key': content_key},
                                                       ExpiresIn=3600)
        style_url = s3_client.generate_presigned_url('get_object',
                                                     Params={'Bucket': S3_BUCKET, 'Key': style_key},
                                                     ExpiresIn=3600)

        # Perform style transfer
        stylized_image = style_transfer(content_url, style_url)

        # Convert to image and save to buffer
        img = Image.fromarray((stylized_image[0] * 255).astype(np.uint8))
        byte_io = io.BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)

        # Clean up S3
        s3_client.delete_object(Bucket=S3_BUCKET, Key=content_key)
        s3_client.delete_object(Bucket=S3_BUCKET, Key=style_key)

        return send_file(byte_io, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))