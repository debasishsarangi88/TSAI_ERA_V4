# 🎵 YouTube Audio Waveform Visualizer

A Flask web application that extracts audio from YouTube videos and creates beautiful waveform visualizations. Perfect for analyzing music, podcasts, or any audio content from YouTube.

## ✨ Features

- **🎥 YouTube Integration**: Extract audio from any YouTube video URL
- **📊 Waveform Visualization**: Beautiful, interactive waveform plots
- **📱 Responsive Design**: Works on desktop and mobile devices
- **⚡ Fast Processing**: Optimized audio processing with librosa
- **📈 Audio Analytics**: Detailed audio information and statistics
- **🎨 Modern UI**: Beautiful gradient design with smooth animations

## 🚀 Quick Start

### Option 1: Local Development

#### 1. Install Dependencies

```bash
# Using UV (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

#### 2. Run the Application

```bash
# Start the Flask server
python app.py
```

#### 3. Open in Browser

Navigate to `http://localhost:8000` and start analyzing YouTube audio!

### Option 2: Using Docker

#### 1. Build and Run with Docker

```bash
# Build the Docker image
docker build -t youtube-waveform-visualizer .

# Run the container
docker run -p 8000:8000 youtube-waveform-visualizer
```

#### 2. Or use Docker Compose

```bash
# Start with Docker Compose
docker-compose up --build

# Stop the services
docker-compose down
```

### Option 3: Using Makefile

```bash
# Install dependencies
make install

# Run the application
make run

# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean up
make clean
```

## 📁 Project Structure

```
├── app.py                    # Main Flask application
├── templates/
│   └── index.html           # Web interface
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_app.py
├── temp_audio/              # Temporary audio files (auto-created)
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup
├── pyproject.toml          # Modern Python packaging
├── Dockerfile              # Docker containerization
├── docker-compose.yml      # Docker Compose configuration
├── Makefile                # Development commands
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── CHANGELOG.md            # Project changelog
├── .github/workflows/      # CI/CD pipeline
│   └── ci.yml
└── README.md               # This file
```

## 🔧 How It Works (Step by Step)

### Step 1: User Input
- User enters a YouTube URL in the web form
- Form is submitted via AJAX to avoid page reload

### Step 2: Audio Download
```python
# Using yt-dlp to download YouTube audio
ydl_opts = {
    'format': 'bestaudio/best',  # Get best audio quality
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',  # Extract audio
        'preferredcodec': 'mp3',      # Convert to MP3
    }],
}
```

### Step 3: Audio Processing
```python
# Load audio with librosa
y, sr = librosa.load(audio_path, sr=None, mono=True)

# Calculate audio properties
duration = librosa.get_duration(y=y, sr=sr)
max_amplitude = np.max(np.abs(y))
rms_energy = np.sqrt(np.mean(y**2))
```

### Step 4: Waveform Generation
```python
# Create matplotlib plot
plt.figure(figsize=(12, 6))
time = np.linspace(0, duration, len(y))
plt.plot(time, y, color='#667eea', linewidth=0.5, alpha=0.8)
```

### Step 5: Display Results
- Waveform image is served to the browser
- Audio statistics are displayed in cards
- Temporary files are cleaned up

## 🛠️ Technical Details

### Dependencies Explained

| Package | Purpose |
|---------|---------|
| `flask` | Web framework for the application |
| `yt-dlp` | Download YouTube videos and extract audio |
| `librosa` | Audio processing and analysis |
| `numpy` | Numerical computations |
| `matplotlib` | Create waveform visualizations |
| `scipy` | Scientific computing (used by librosa) |

### Key Functions

#### `download_youtube_audio(url, output_path)`
- Downloads audio from YouTube using yt-dlp
- Converts to MP3 format
- Handles errors gracefully

#### `create_waveform_plot(audio_path, output_path)`
- Loads audio file with librosa
- Creates matplotlib visualization
- Returns audio statistics

#### `analyze_audio()` (Flask route)
- Handles form submission
- Orchestrates the entire process
- Returns JSON response

## 🎯 Usage Examples

### Basic Usage
1. Open the web interface
2. Paste a YouTube URL
3. Click "Analyze Audio & Generate Waveform"
4. View the results!

### Example URLs to Try
- Rick Astley - Never Gonna Give You Up
- PSY - GANGNAM STYLE
- Luis Fonsi - Despacito
- Ed Sheeran - Shape of You

## 📊 Audio Information Displayed

The application shows:
- **Duration**: Length of the audio in seconds
- **Sample Rate**: Audio quality (typically 44.1kHz)
- **Total Samples**: Number of audio data points
- **Max Amplitude**: Peak audio level
- **RMS Energy**: Average audio energy

## 🔍 Understanding the Waveform

### What the Waveform Shows
- **X-axis**: Time (seconds)
- **Y-axis**: Amplitude (audio intensity)
- **Peaks**: Loud parts of the audio
- **Valleys**: Quiet parts of the audio
- **Patterns**: Musical structure, beats, etc.

### Interpreting the Visualization
- **Dense sections**: Complex audio (music, speech)
- **Sparse sections**: Silence or quiet parts
- **Regular patterns**: Rhythmic content (music)
- **Irregular patterns**: Speech or varied content

## 🛡️ Error Handling

The application handles various errors:
- Invalid YouTube URLs
- Network connectivity issues
- Audio processing errors
- File system problems

## 🔧 Customization

### Changing Waveform Style
Edit the `create_waveform_plot()` function in `app.py`:

```python
# Change colors
plt.plot(time, y, color='#ff6b6b', linewidth=1.0, alpha=0.9)

# Change plot size
plt.figure(figsize=(15, 8))

# Add more styling
plt.grid(True, alpha=0.5)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
```

### Adding More Audio Analysis
Extend the audio information in `create_waveform_plot()`:

```python
# Add spectral centroid
spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]

# Add tempo estimation
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

return {
    'duration': round(duration, 2),
    'tempo': round(tempo, 2),
    'spectral_centroid_mean': float(np.mean(spectral_centroids)),
    # ... other properties
}
```

## 🚨 Important Notes

### Legal Considerations
- Only use this tool for content you have permission to analyze
- Respect YouTube's Terms of Service
- Don't download copyrighted content without permission

### Technical Limitations
- Processing time depends on video length
- Large videos may take longer to process
- Some videos may be restricted or unavailable

### System Requirements
- Python 3.8+
- Sufficient disk space for temporary files
- Internet connection for YouTube access

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to download audio"**
   - Check internet connection
   - Verify YouTube URL is valid
   - Try a different video

2. **"No module named 'librosa'"**
   - Install dependencies: `pip install -r requirements.txt`
   - Use virtual environment

3. **Slow processing**
   - Longer videos take more time
   - Check system resources
   - Consider shorter videos for testing

### Debug Mode
Run with debug enabled:
```bash
export FLASK_ENV=development
python app.py
```

## 🤝 Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws.

---

**Built with ❤️ for TSAI ERA V4 Session 2**

*Enjoy analyzing your favorite YouTube audio! 🎵*
