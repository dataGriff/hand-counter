#!/usr/bin/env python3
import cv2
import numpy as np

# Load the test image
image = cv2.imread('/tmp/realistic_test.jpg')
image_vis = image.copy()

# Detections from previous run
detections = [
    ([289, 90, 321, 642], False, "Person 1"),
    ([0, 87, 320, 676], False, "Person 2?"),
    ([577, 81, 341, 682], False, "Person 3"),
    ([516, 69, 226, 452], False, "Person 4"),
    ([160, 68, 226, 452], False, "Person 5"),
]

# Draw bounding boxes
for bbox, hands_raised, label in detections:
    x, y, w, h = bbox
    color = (0, 255, 0) if hands_raised else (0, 0, 255)
    cv2.rectangle(image_vis, (x, y), (x+w, y+h), color, 2)
    
    # Draw the upper 40% region boundary
    upper_h = int(h * 0.4)
    cv2.line(image_vis, (x, y+upper_h), (x+w, y+upper_h), (255, 0, 255), 2)
    
    # Label
    cv2.putText(image_vis, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

cv2.imwrite('/tmp/detections_visualization.jpg', image_vis)
print("Saved visualization to /tmp/detections_visualization.jpg")

# Now let's check where the actual raised hands are in our synthetic image
print("\nIn our synthetic image:")
print("  Person 2 (center, hands UP) was drawn at x=450")
print("  - Head at y=200")
print("  - Raised arms from y=120 to y=250 (y-80 to y+50)")
print("  - Hands at y=120 (y-80)")
print("\n  Detected bbox for person near center: x=577, y=81")
print("  This should capture the raised hands IF the bbox extends high enough")

# Check if the y-coordinate is low enough to capture raised hands
print("\n  Person at x=450 was drawn with hands at y=120")
print("  Closest detection has y=81, which is ABOVE the hands!")
print("  So the bbox DOES include the raised hands region")

print("\nThe issue is likely with how we're analyzing the region.")
print("Let me check if we should look for raised hands ABOVE the person,")
print("not just in the upper portion of the bbox...")
