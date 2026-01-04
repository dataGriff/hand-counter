#!/usr/bin/env python3
"""
Web application for Hand Counter
Provides a stateless web interface for counting people and raised hands in images.
"""

from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import tempfile
from io import BytesIO
from PIL import Image
import base64
from hand_counter import HandCounter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_image():
    """
    Analyze uploaded image for people and raised hands.
    Stateless endpoint - processes image in memory without storing anything.
    """
    temp_path = None
    try:
        # Check if image was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Read image from upload (stateless - in memory only)
        image_bytes = file.read()
        
        # Convert to numpy array for OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Create unique temporary file for processing
        fd, temp_path = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)  # Close the file descriptor
        
        # Save to temporary file for processing
        cv2.imwrite(temp_path, image)
        
        # Process the image
        counter = HandCounter()
        results = counter.process_image(temp_path)
        
        # Return results as JSON
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
