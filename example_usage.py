#!/usr/bin/env python3
"""
Example usage of the Hand Counter application.
Demonstrates how to use the HandCounter class programmatically.
"""

from hand_counter import HandCounter


def main():
    """Example usage of the HandCounter class."""
    
    # Initialize the counter
    counter = HandCounter()
    
    # Example 1: Process a single image
    print("Example 1: Processing an image")
    print("-" * 40)
    
    image_path = "path/to/your/image.jpg"
    print(f"Image path: {image_path}")
    print("\nNote: Replace with actual image path to test")
    
    # Uncomment the following lines when you have a real image:
    # try:
    #     results = counter.process_image(image_path)
    #     
    #     print(f"\nResults:")
    #     print(f"  Total people: {results['total_people']}")
    #     print(f"  Hands raised: {results['hands_raised']}")
    #     print(f"  Hands down: {results['hands_down']}")
    #     print(f"\nProportions:")
    #     print(f"  Raised: {results['hands_raised_proportion']:.1f}%")
    #     print(f"  Down: {results['hands_down_proportion']:.1f}%")
    # except Exception as e:
    #     print(f"Error: {e}")
    
    print("\n" + "=" * 40)
    print("\nTo use this example:")
    print("1. Replace 'path/to/your/image.jpg' with an actual image")
    print("2. Uncomment the try/except block")
    print("3. Run: python example_usage.py")
    print("\nOr use the CLI directly:")
    print("  python hand_counter.py your_image.jpg")


if __name__ == "__main__":
    main()
