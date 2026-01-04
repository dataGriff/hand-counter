# Hand Counter 🙋

An intelligent image analysis application that counts the number of people in an image and detects how many have their hands raised. Provides detailed statistics including counts and proportions.

## Features

- 📷 Processes images to detect people
- 🙋 Identifies people with raised hands using image analysis
- 📊 Calculates proportions of people with hands raised vs. hands down
- 🎯 Supports multiple people in a single image
- 💻 Simple command-line interface

## Requirements

- Python 3.7 or higher
- OpenCV
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dataGriff/hand-counter-.git
cd hand-counter-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python hand_counter.py path/to/image.jpg
```

### Example Output

```
Processing image: photo.jpg
Detecting people and analyzing hand positions...

==================================================
HAND COUNTER RESULTS
==================================================

Total people detected: 1

People with hands raised: 1
People with hands down: 0

Proportions:
  - Hands raised: 100.0%
  - Hands down: 0.0%
==================================================
```

## How It Works

1. **Person Detection**: The application uses OpenCV's HOG (Histogram of Oriented Gradients) detector to identify people in the image.

2. **Hand Position Analysis**: For each detected person, the application analyzes the upper portion of their bounding box using edge detection and image processing techniques.

3. **Raised Hand Detection**: A heuristic approach checks for significant activity (edges/features) in the upper region of each person's bounding box, which typically indicates raised hands.

4. **Statistics Calculation**: The app calculates:
   - Total number of people
   - Number of people with hands raised
   - Number of people with hands down
   - Percentage proportions of each

## Limitations

- Detection accuracy depends on image quality, lighting, and camera angle
- People must be clearly visible with their upper body shown
- Works best with frontal or semi-frontal views
- Very crowded scenes may reduce accuracy
- The hand-raising detection uses heuristic methods that work well for typical scenarios but may have limitations with unusual poses or clothing

## Technical Details

- Uses OpenCV HOG detector for person detection
- Employs edge detection and density analysis for raised hand detection
- Processes images in BGR color space
- Configurable detection parameters for different scenarios

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
