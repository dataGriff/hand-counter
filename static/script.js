// DOM elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const analyzeAnotherBtn = document.getElementById('analyzeAnotherBtn');
const retryBtn = document.getElementById('retryBtn');

let selectedFile = null;

// Upload area click handler
uploadArea.addEventListener('click', () => {
    imageInput.click();
});

// File input change handler
imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFileSelect(file);
    }
});

// Handle file selection
function handleFileSelect(file) {
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        analyzeBtn.style.display = 'block';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Clear button handler
clearBtn.addEventListener('click', () => {
    resetUpload();
});

// Analyze button handler
analyzeBtn.addEventListener('click', () => {
    if (!selectedFile) return;
    
    analyzeImage();
});

// Analyze another button handler
analyzeAnotherBtn.addEventListener('click', () => {
    resetUpload();
});

// Retry button handler
retryBtn.addEventListener('click', () => {
    errorSection.style.display = 'none';
    previewSection.style.display = 'block';
    analyzeBtn.style.display = 'block';
});

// Reset upload state
function resetUpload() {
    selectedFile = null;
    imageInput.value = '';
    uploadArea.style.display = 'block';
    previewSection.style.display = 'none';
    analyzeBtn.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    loading.style.display = 'none';
}

// Analyze image
async function analyzeImage() {
    // Show loading
    previewSection.style.display = 'none';
    analyzeBtn.style.display = 'none';
    loading.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('image', selectedFile);
        
        // Send request
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze image');
        }
        
        // Hide loading
        loading.style.display = 'none';
        
        // Display results
        displayResults(data.results, data.annotated_image);
        
    } catch (error) {
        loading.style.display = 'none';
        showError(error.message);
    }
}

// Display results
function displayResults(results, annotatedImage) {
    // Update stats
    document.getElementById('totalPeople').textContent = results.total_people;
    document.getElementById('handsRaised').textContent = results.hands_raised;
    document.getElementById('handsDown').textContent = results.hands_down;
    
    // Update proportion bar
    const raisedPercent = results.hands_raised_proportion;
    const downPercent = results.hands_down_proportion;
    
    const raisedBar = document.getElementById('proportionRaisedBar');
    const downBar = document.getElementById('proportionDownBar');
    
    raisedBar.style.width = raisedPercent + '%';
    downBar.style.width = downPercent + '%';
    
    document.getElementById('proportionRaisedText').textContent = raisedPercent.toFixed(1) + '%';
    document.getElementById('proportionDownText').textContent = downPercent.toFixed(1) + '%';
    
    // Display annotated image if available
    const annotatedImageSection = document.getElementById('annotatedImageSection');
    const annotatedImageElement = document.getElementById('annotatedImage');
    if (annotatedImage) {
        annotatedImageElement.src = annotatedImage;
        annotatedImageSection.style.display = 'block';
    } else {
        annotatedImageSection.style.display = 'none';
    }
    
    // Show results
    resultsSection.style.display = 'block';
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}
