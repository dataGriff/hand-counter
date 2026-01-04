#!/usr/bin/env python3
"""
Hand Counter Application
Counts the number of people in an image and how many have their hands raised.
"""

import argparse
import cv2
import numpy as np
from pathlib import Path


class HandCounter:
    """Counts people and raised hands in images using pose estimation."""
    
    def __init__(self):
        """Initialize OpenCV DNN with a pre-trained person detection model."""
        # For simplicity, we'll use OpenCV's HOG detector and simple heuristics
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    def detect_raised_hands_heuristic(self, image, bbox):
        """
        Heuristic method to detect if hands are raised in a bounding box.
        Uses color and position analysis in the upper portion of the detected person.
        
        Args:
            image: The full image (BGR format)
            bbox: Bounding box (x, y, w, h) of the detected person
            
        Returns:
            bool: True if likely has hands raised, False otherwise
        """
        x, y, w, h = bbox
        
        # Check if the person's upper body area has significant motion/presence
        # This is a simplified heuristic that checks the upper 40% of the bounding box
        upper_region_height = int(h * 0.4)
        upper_region = image[y:y+upper_region_height, x:x+w]
        
        if upper_region.size == 0:
            return False
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(upper_region, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection in the upper region
        edges = cv2.Canny(gray, 50, 150)
        
        # Calculate the density of edges in the upper region
        edge_density = np.sum(edges > 0) / edges.size
        
        # If there's significant edge density in upper region, likely hands are raised
        # This is a simple heuristic - adjust threshold as needed
        return edge_density > 0.05
    
    def non_max_suppression(self, boxes, weights, overlap_threshold=0.35):
        """
        Apply non-maximum suppression to remove overlapping detections.
        
        Args:
            boxes: Array of bounding boxes (x, y, w, h)
            weights: Detection confidence weights
            overlap_threshold: IoU threshold for suppression
            
        Returns:
            tuple: Filtered boxes and weights
        """
        if len(boxes) == 0:
            return np.array([]), np.array([])
        
        # Convert boxes to (x1, y1, x2, y2) format
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 0] + boxes[:, 2]
        y2 = boxes[:, 1] + boxes[:, 3]
        
        areas = boxes[:, 2] * boxes[:, 3]
        order = weights.flatten().argsort()[::-1]
        
        keep = []
        while len(order) > 0:
            i = order[0]
            keep.append(i)
            
            # Compute IoU with remaining boxes
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            
            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            
            intersection = w * h
            union = areas[i] + areas[order[1:]] - intersection
            
            # Handle division by zero - if union is 0, boxes are identical (IoU = 1.0)
            iou = np.where(union > 0, intersection / union, 1.0)
            
            # Keep only boxes with IoU less than threshold
            order = order[np.where(iou <= overlap_threshold)[0] + 1]
        
        return boxes[keep], weights[keep]
    
    def process_image(self, image_path):
        """
        Process an image to count people and raised hands.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Results containing counts and proportions, plus detection details
        """
        # Load image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Detect people in the image with more sensitive parameters
        boxes, weights = self.hog.detectMultiScale(
            image, 
            winStride=(4, 4),      # Keep standard for balance between speed and accuracy
            padding=(4, 4),         # Reduced from (8, 8) for less padding
            scale=1.03,             # Reduced from 1.05 for better multi-scale detection
            hitThreshold=-0.3       # Lowered from 0 to detect more candidates while reducing false positives
        )
        
        # Filter out low-confidence detections
        if len(boxes) > 0:
            confidence_threshold = 0.3
            mask = weights.flatten() > confidence_threshold
            boxes = boxes[mask]
            weights = weights[mask]
        
        # Apply non-maximum suppression to remove overlapping detections
        if len(boxes) > 0:
            boxes, weights = self.non_max_suppression(boxes, weights)
        
        total_people = len(boxes)
        hands_raised_count = 0
        detections = []
        
        # Analyze each detected person
        for bbox in boxes:
            hands_raised = self.detect_raised_hands_heuristic(image, bbox)
            if hands_raised:
                hands_raised_count += 1
            
            # Store detection details (convert numpy types to Python native types)
            detections.append({
                'bbox': bbox.tolist() if isinstance(bbox, np.ndarray) else list(bbox),
                'hands_raised': bool(hands_raised)
            })
        
        # Calculate proportions
        hands_raised_proportion = (hands_raised_count / total_people * 100 
                                  if total_people > 0 else 0)
        hands_down_proportion = 100 - hands_raised_proportion
        
        return {
            'total_people': total_people,
            'hands_raised': hands_raised_count,
            'hands_down': total_people - hands_raised_count,
            'hands_raised_proportion': hands_raised_proportion,
            'hands_down_proportion': hands_down_proportion,
            'detections': detections
        }


def print_results(results):
    """Print the results in a formatted way."""
    print("\n" + "="*50)
    print("HAND COUNTER RESULTS")
    print("="*50)
    print(f"\nTotal people detected: {results['total_people']}")
    print(f"\nPeople with hands raised: {results['hands_raised']}")
    print(f"People with hands down: {results['hands_down']}")
    print(f"\nProportions:")
    print(f"  - Hands raised: {results['hands_raised_proportion']:.1f}%")
    print(f"  - Hands down: {results['hands_down_proportion']:.1f}%")
    print("="*50 + "\n")


def main():
    """Main function to run the hand counter application."""
    parser = argparse.ArgumentParser(
        description='Count people and raised hands in an image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hand_counter.py image.jpg
  python hand_counter.py photo.png
        """
    )
    parser.add_argument('image', type=str, help='Path to the image file')
    
    args = parser.parse_args()
    
    # Validate image path
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Error: Image file not found: {image_path}")
        return 1
    
    # Process image
    print(f"Processing image: {image_path}")
    counter = HandCounter()
    
    try:
        print("Detecting people and analyzing hand positions...")
        results = counter.process_image(str(image_path))
        
        print_results(results)
        return 0
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
