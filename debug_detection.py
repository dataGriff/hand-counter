#!/usr/bin/env python3
import cv2
import numpy as np
from hand_counter import HandCounter

# Create a more realistic test image
def create_realistic_test_image():
    """Create a test image that mimics a classroom scenario"""
    # Create a white background
    img = np.ones((800, 1200, 3), dtype=np.uint8) * 240
    
    # Person 1 - hands down (left)
    x1, y1 = 150, 200
    # Head
    cv2.circle(img, (x1, y1), 50, (80, 80, 80), -1)
    # Body
    cv2.rectangle(img, (x1-60, y1+50), (x1+60, y1+250), (100, 100, 100), -1)
    # Arms down
    cv2.rectangle(img, (x1-120, y1+80), (x1-60, y1+250), (100, 100, 100), -1)
    cv2.rectangle(img, (x1+60, y1+80), (x1+120, y1+250), (100, 100, 100), -1)
    # Legs
    cv2.rectangle(img, (x1-50, y1+250), (x1-10, y1+450), (80, 80, 80), -1)
    cv2.rectangle(img, (x1+10, y1+250), (x1+50, y1+450), (80, 80, 80), -1)
    
    # Person 2 - hands UP (center)
    x2, y2 = 450, 200
    # Head
    cv2.circle(img, (x2, y2), 50, (80, 80, 80), -1)
    # Body
    cv2.rectangle(img, (x2-60, y2+50), (x2+60, y2+250), (100, 100, 100), -1)
    # Arms UP (higher position)
    cv2.rectangle(img, (x2-120, y2-80), (x2-60, y2+50), (100, 100, 100), -1)
    cv2.rectangle(img, (x2+60, y2-80), (x2+120, y2+50), (100, 100, 100), -1)
    # Hands at top
    cv2.circle(img, (x2-90, y2-80), 25, (120, 120, 120), -1)
    cv2.circle(img, (x2+90, y2-80), 25, (120, 120, 120), -1)
    # Legs
    cv2.rectangle(img, (x2-50, y2+250), (x2-10, y2+450), (80, 80, 80), -1)
    cv2.rectangle(img, (x2+10, y2+250), (x2+50, y2+450), (80, 80, 80), -1)
    
    # Person 3 - hands down (right)
    x3, y3 = 750, 200
    # Head
    cv2.circle(img, (x3, y3), 50, (80, 80, 80), -1)
    # Body
    cv2.rectangle(img, (x3-60, y3+50), (x3+60, y3+250), (100, 100, 100), -1)
    # Arms down
    cv2.rectangle(img, (x3-120, y3+80), (x3-60, y3+250), (100, 100, 100), -1)
    cv2.rectangle(img, (x3+60, y3+80), (x3+120, y3+250), (100, 100, 100), -1)
    # Legs
    cv2.rectangle(img, (x3-50, y3+250), (x3-10, y3+450), (80, 80, 80), -1)
    cv2.rectangle(img, (x3+10, y3+250), (x3+50, y3+450), (80, 80, 80), -1)
    
    # Person 4 - hands down (back left)
    x4, y4 = 280, 150
    scale = 0.7
    # Head
    cv2.circle(img, (x4, y4), int(40*scale), (70, 70, 70), -1)
    # Body
    cv2.rectangle(img, (x4-int(50*scale), y4+int(40*scale)), 
                  (x4+int(50*scale), y4+int(200*scale)), (90, 90, 90), -1)
    # Arms down
    cv2.rectangle(img, (x4-int(90*scale), y4+int(60*scale)), 
                  (x4-int(50*scale), y4+int(200*scale)), (90, 90, 90), -1)
    cv2.rectangle(img, (x4+int(50*scale), y4+int(60*scale)), 
                  (x4+int(90*scale), y4+int(200*scale)), (90, 90, 90), -1)
    
    # Person 5 - hands down (back right)
    x5, y5 = 620, 150
    # Head
    cv2.circle(img, (x5, y5), int(40*scale), (70, 70, 70), -1)
    # Body
    cv2.rectangle(img, (x5-int(50*scale), y5+int(40*scale)), 
                  (x5+int(50*scale), y5+int(200*scale)), (90, 90, 90), -1)
    # Arms down
    cv2.rectangle(img, (x5-int(90*scale), y5+int(60*scale)), 
                  (x5-int(50*scale), y5+int(200*scale)), (90, 90, 90), -1)
    cv2.rectangle(img, (x5+int(50*scale), y5+int(60*scale)), 
                  (x5+int(90*scale), y5+int(200*scale)), (90, 90, 90), -1)
    
    return img

# Create and save test image
test_img = create_realistic_test_image()
cv2.imwrite('/tmp/realistic_test.jpg', test_img)
print("Created test image: /tmp/realistic_test.jpg")

# Test the counter
counter = HandCounter()
results = counter.process_image('/tmp/realistic_test.jpg')

print("\n" + "="*50)
print("DETECTION RESULTS")
print("="*50)
print(f"Total people detected: {results['total_people']}")
print(f"People with hands raised: {results['hands_raised']}")
print(f"People with hands down: {results['hands_down']}")
print(f"\nExpected: 5 people total, 1 hands up, 4 hands down")
print("="*50)

# Debug: Show details for each detection
print("\nDetection details:")
for i, detection in enumerate(results['detections']):
    bbox = detection['bbox']
    hands_raised = detection['hands_raised']
    print(f"  Person {i+1}: bbox={bbox}, hands_raised={hands_raised}")
