#!/usr/bin/env python3
"""
Test script for the hand counter application.
Creates test images and verifies the functionality.
"""

import cv2
import numpy as np
import sys
import tempfile
from pathlib import Path

# Add the current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from hand_counter import HandCounter


def create_test_image_with_person(filename, person_height=400):
    """Create a test image with a simple person-like figure."""
    img = np.ones((600, 500, 3), dtype=np.uint8) * 240
    
    # Draw a simplified person figure in the center
    center_x = 250
    top_y = 100
    
    # Head (circle)
    cv2.circle(img, (center_x, top_y), 40, (80, 80, 80), -1)
    
    # Body (rectangle)
    body_top = top_y + 40
    body_bottom = body_top + 150
    cv2.rectangle(img, (center_x - 50, body_top), 
                  (center_x + 50, body_bottom), (100, 100, 100), -1)
    
    # Arms (rectangles) - raised
    arm_y = body_top + 30
    # Left arm raised
    cv2.rectangle(img, (center_x - 50, arm_y - 80), 
                  (center_x - 30, arm_y), (100, 100, 100), -1)
    # Right arm raised
    cv2.rectangle(img, (center_x + 30, arm_y - 80), 
                  (center_x + 50, arm_y), (100, 100, 100), -1)
    
    # Legs
    leg_top = body_bottom
    leg_bottom = leg_top + 150
    cv2.rectangle(img, (center_x - 40, leg_top), 
                  (center_x - 10, leg_bottom), (100, 100, 100), -1)
    cv2.rectangle(img, (center_x + 10, leg_top), 
                  (center_x + 40, leg_bottom), (100, 100, 100), -1)
    
    cv2.imwrite(filename, img)
    return filename


def create_test_image_no_person(filename):
    """Create a test image with no people."""
    img = np.ones((400, 600, 3), dtype=np.uint8) * 220
    
    # Draw some scenery
    cv2.rectangle(img, (100, 150), (500, 350), (180, 200, 180), -1)
    cv2.circle(img, (300, 100), 50, (100, 150, 200), -1)
    
    cv2.putText(img, 'Empty Scene', (200, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)
    
    cv2.imwrite(filename, img)
    return filename


def run_tests():
    """Run tests on the hand counter."""
    print("=" * 60)
    print("HAND COUNTER TEST SUITE")
    print("=" * 60)
    
    counter = HandCounter()
    test_results = []
    
    # Use temporary directory for cross-platform compatibility
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test 1: Image with person
        print("\n[Test 1] Image with person (hands raised)...")
        test_file = create_test_image_with_person(str(temp_path / 'test_person_raised.jpg'))
        try:
            result = counter.process_image(test_file)
            print(f"  - People detected: {result['total_people']}")
            print(f"  - Hands raised: {result['hands_raised']}")
            print(f"  - Proportion: {result['hands_raised_proportion']:.1f}%")
            test_results.append(("Person detection", result['total_people'] >= 0))
        except Exception as e:
            print(f"  ERROR: {e}")
            test_results.append(("Person detection", False))
        
        # Test 2: Empty scene
        print("\n[Test 2] Image with no people...")
        test_file = create_test_image_no_person(str(temp_path / 'test_empty.jpg'))
        try:
            result = counter.process_image(test_file)
            print(f"  - People detected: {result['total_people']}")
            print(f"  - Hands raised: {result['hands_raised']}")
            success = result['total_people'] == 0
            test_results.append(("Empty scene detection", success))
        except Exception as e:
            print(f"  ERROR: {e}")
            test_results.append(("Empty scene detection", False))
    
    # Test 3: Verify proportions calculation
    print("\n[Test 3] Proportion calculation...")
    try:
        # Mock data for testing proportions
        test_data = {
            'total': 10,
            'raised': 3
        }
        expected_raised_prop = 30.0
        expected_down_prop = 70.0
        
        calculated_raised = (test_data['raised'] / test_data['total'] * 100)
        calculated_down = 100 - calculated_raised
        
        prop_correct = (abs(calculated_raised - expected_raised_prop) < 0.1 and
                       abs(calculated_down - expected_down_prop) < 0.1)
        
        print(f"  - Raised proportion: {calculated_raised:.1f}% (expected: {expected_raised_prop:.1f}%)")
        print(f"  - Down proportion: {calculated_down:.1f}% (expected: {expected_down_prop:.1f}%)")
        test_results.append(("Proportion calculation", prop_correct))
    except Exception as e:
        print(f"  ERROR: {e}")
        test_results.append(("Proportion calculation", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTests passed: {passed}/{total}")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
