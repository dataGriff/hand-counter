# Hand Counter 🙋

An intelligent image analysis application that counts the number of people in an image and detects how many have their hands raised. Provides detailed statistics including counts and proportions.

Available as both a **CLI tool** and a **web application**.

## Features

- 📷 Processes images to detect people
- 🙋 Identifies people with raised hands using image analysis
- 📊 Calculates proportions of people with hands raised vs. hands down
- 🎯 Supports multiple people in a single image
- 💻 Simple command-line interface
- 🌐 Stateless web application for easy deployment

## Requirements

- Python 3.7 or higher
- OpenCV
- NumPy
- Flask (for web app)
- Pillow (for web app)

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

### Web Application (Recommended)

Start the web server:

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

The web application provides:
- Drag-and-drop or click-to-upload interface
- Real-time image analysis
- Visual results with charts and statistics
- **Completely stateless** - no images are stored on the server

### Command Line Interface

```bash
python hand_counter.py path/to/image.jpg
```

### Example Output (CLI)

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

## Deployment

### 🚀 Free & Easy Deployment (Recommended)

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed step-by-step guides to deploy for free on:

- **Render** (Recommended) - One-click deploy from GitHub
- **Railway** - Simple deployment with $5 free credit
- **Fly.io** - Global edge deployment
- **PythonAnywhere** - Python-focused hosting

All options include free HTTPS and are perfect for personal projects!

### Local Development

```bash
python app.py
```

### Production Deployment

For production deployment, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

Build and run:

```bash
docker build -t hand-counter .
docker run -p 8000:8000 hand-counter
```

### Cloud Deployment

The application can be deployed to various cloud platforms:

- **Heroku**: Add a `Procfile` with `web: gunicorn app:app`
- **Google Cloud Run**: Use the Dockerfile above
- **AWS Elastic Beanstalk**: Deploy as a Python application
- **Azure App Service**: Deploy as a Python web app

## How It Works

1. **Person Detection**: The application uses OpenCV's HOG (Histogram of Oriented Gradients) detector to identify people in the image.

2. **Hand Position Analysis**: For each detected person, the application analyzes the upper portion of their bounding box using edge detection and image processing techniques.

3. **Raised Hand Detection**: A heuristic approach checks for significant activity (edges/features) in the upper region of each person's bounding box, which typically indicates raised hands.

4. **Statistics Calculation**: The app calculates:
   - Total number of people
   - Number of people with hands raised
   - Number of people with hands down
   - Percentage proportions of each

## Stateless Architecture

The web application is designed to be completely stateless:
- Images are processed in memory only
- No files are saved to disk (except temporary processing)
- No database or persistent storage required
- Easily scalable horizontally

## Limitations

- Detection accuracy depends on image quality, lighting, and camera angle
- People must be clearly visible with their upper body shown
- Works best with frontal or semi-frontal views
- In very crowded scenes with heavy occlusion, some people may not be detected
- The hand-raising detection uses heuristic methods that work well for typical scenarios but may have limitations with unusual poses or clothing
- The HOG detector is optimized for real photographs and may have varying results with synthetic/drawn images

## Technical Details

- Uses OpenCV HOG detector for person detection with optimized parameters for crowded scenes
- Implements non-maximum suppression (NMS) to filter overlapping detections
- Applies confidence thresholding to reduce false positives

- Uses OpenCV HOG detector for person detection
- Employs edge detection and density analysis for raised hand detection
- Processes images in BGR color space
- Configurable detection parameters for different scenarios
- Flask-based REST API for web interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
