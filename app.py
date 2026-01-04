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

# Marker sizing constants
MARKER_MAX_RADIUS = 25
MARKER_MIN_RADIUS_DIVISOR = 6
MARKER_OFFSET_MAX = 40
MARKER_OFFSET_DIVISOR = 4
MARKER_OFFSET_PADDING = 10


def annotate_image(image, detections):
    """
    Annotate image with bounding boxes and markers for raised/not raised hands.
    
    Args:
        image: OpenCV image (BGR format)
        detections: List of detection dicts with 'bbox' and 'hands_raised' keys
        
    Returns:
        Annotated OpenCV image
    """
    annotated = image.copy()
    
    for detection in detections:
        bbox = detection.get('bbox')
        if not bbox or len(bbox) != 4:
            continue  # Skip invalid bounding boxes
            
        hands_raised = detection.get('hands_raised', False)
        
        x, y, w, h = bbox
        
        # Draw bounding box
        box_color = (0, 255, 0) if hands_raised else (0, 0, 255)  # Green for raised, red for down
        cv2.rectangle(annotated, (x, y), (x + w, y + h), box_color, 3)
        
        # Calculate marker position (top-right corner of bounding box)
        # Use relative positioning based on bounding box size
        marker_radius = min(MARKER_MAX_RADIUS, min(w, h) // MARKER_MIN_RADIUS_DIVISOR)
        marker_offset = max(marker_radius + MARKER_OFFSET_PADDING, 
                           min(MARKER_OFFSET_MAX, w // MARKER_OFFSET_DIVISOR))
        marker_x = x + w - marker_offset
        marker_y = y + marker_offset
        
        if hands_raised:
            # Draw green circle background
            cv2.circle(annotated, (marker_x, marker_y), marker_radius, (0, 200, 0), -1)
            cv2.circle(annotated, (marker_x, marker_y), marker_radius, (0, 255, 0), 2)
            
            # Draw checkmark (tick) - scaled relative to marker radius
            tick_size = int(marker_radius * 0.6)
            # Short line of checkmark
            cv2.line(annotated, 
                    (marker_x - tick_size // 2, marker_y), 
                    (marker_x - tick_size // 6, marker_y + tick_size // 2), 
                    (255, 255, 255), max(2, marker_radius // 8))
            # Long line of checkmark
            cv2.line(annotated, 
                    (marker_x - tick_size // 6, marker_y + tick_size // 2), 
                    (marker_x + tick_size // 2, marker_y - tick_size // 2), 
                    (255, 255, 255), max(2, marker_radius // 8))
        else:
            # Draw red circle background
            cv2.circle(annotated, (marker_x, marker_y), marker_radius, (0, 0, 200), -1)
            cv2.circle(annotated, (marker_x, marker_y), marker_radius, (0, 0, 255), 2)
            
            # Draw X (cross) - scaled relative to marker radius
            cross_size = int(marker_radius * 0.6)
            cv2.line(annotated, 
                    (marker_x - cross_size // 2, marker_y - cross_size // 2), 
                    (marker_x + cross_size // 2, marker_y + cross_size // 2), 
                    (255, 255, 255), max(2, marker_radius // 8))
            cv2.line(annotated, 
                    (marker_x - cross_size // 2, marker_y + cross_size // 2), 
                    (marker_x + cross_size // 2, marker_y - cross_size // 2), 
                    (255, 255, 255), max(2, marker_radius // 8))
    
    return annotated


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
        
        # Annotate the image with markers
        annotated_image = annotate_image(image, results.get('detections', []))
        
        # Convert annotated image to base64
        _, buffer = cv2.imencode('.jpg', annotated_image)
        annotated_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Return results as JSON
        return jsonify({
            'success': True,
            'results': results,
            'annotated_image': f'data:image/jpeg;base64,{annotated_base64}'
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
