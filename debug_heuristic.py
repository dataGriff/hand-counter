#!/usr/bin/env python3
import cv2
import numpy as np

# Load the test image
image = cv2.imread('/tmp/realistic_test.jpg')

# Use the detected bounding boxes from the previous run
# Person 2 (hands UP) had bbox=[577, 81, 341, 682]
bbox_hands_up = [577, 81, 341, 682]
# Person 1 (hands DOWN) had bbox=[289, 90, 321, 642]
bbox_hands_down = [289, 90, 321, 642]

def analyze_bbox(image, bbox, label):
    """Analyze a bounding box in detail"""
    x, y, w, h = bbox
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {label}")
    print(f"BBox: x={x}, y={y}, w={w}, h={h}")
    print(f"{'='*60}")
    
    # Extract upper 40% region (current approach)
    upper_region_height = int(h * 0.4)
    upper_region = image[y:y+upper_region_height, x:x+w]
    
    print(f"Upper region (40% of height = {upper_region_height}px):")
    print(f"  Region from y={y} to y={y+upper_region_height}")
    
    if upper_region.size == 0:
        print("  ERROR: Empty region!")
        return
    
    # Convert to grayscale
    gray = cv2.cvtColor(upper_region, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Calculate edge density
    edge_density = np.sum(edges > 0) / edges.size
    
    print(f"  Edge density: {edge_density:.4f}")
    print(f"  Threshold: 0.05")
    print(f"  Classification: {'HANDS UP' if edge_density > 0.05 else 'HANDS DOWN'}")
    
    # Save visualization
    cv2.imwrite(f'/tmp/debug_{label.replace(" ", "_")}_region.jpg', upper_region)
    cv2.imwrite(f'/tmp/debug_{label.replace(" ", "_")}_edges.jpg', edges)
    print(f"  Saved visualization to /tmp/debug_{label.replace('  ', '_')}*.jpg")

# Analyze both cases
analyze_bbox(image, bbox_hands_down, "Person 1 (hands down)")
analyze_bbox(image, bbox_hands_up, "Person 2 (hands up)")

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("The heuristic checks for edge density in the UPPER 40% of bbox.")
print("High edge density = more activity = hands raised")
print("Low edge density = less activity = hands down")
print("\nIf both are showing as 'hands down', the threshold may be too high,")
print("or the edge detection isn't capturing the raised hands properly.")
print("="*60)
