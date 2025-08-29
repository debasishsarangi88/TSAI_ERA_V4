#!/usr/bin/env python3
"""
YouTube Audio Waveform Visualizer
A Flask web application that extracts audio from YouTube videos and displays the waveform.
"""

# Import necessary libraries
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp  # For downloading YouTube videos
import librosa  # For audio processing
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For creating plots
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web
import os
import tempfile
import uuid
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure app settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_audio'  # Folder to store temporary audio files

# EC2 and production settings
app.config['DEBUG'] = False  # Set to False for production
app.config['HOST'] = '0.0.0.0'  # Listen on all interfaces
app.config['PORT'] = 5000  # Use port 5000

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Configure logging for EC2
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("YouTube Audio Waveform Visualizer starting up...")

def download_youtube_audio(url, output_path):
    """
    Download audio from YouTube URL using yt-dlp with anti-bot measures
    
    Args:
        url (str): YouTube video URL
        output_path (str): Path where to save the audio file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Starting download for URL: {url}")
        
        # Configure yt-dlp options with anti-bot measures
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
            'outtmpl': output_path,
            'quiet': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
            },
            'extractor_retries': 5,
            'retries': 5,
            'fragment_retries': 5,
            'no_check_certificate': True,
            'ignoreerrors': False,
            'nocheckcertificate': True,
        }
        
        print(f"yt-dlp options configured with anti-bot measures")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("yt-dlp instance created, starting download...")
            ydl.download([url])
        
        # Check if any file was actually downloaded
        for ext in ['.m4a', '.webm', '.mp3', '.wav']:
            test_path = output_path + ext
            if os.path.exists(test_path):
                print(f"Successfully downloaded: {test_path}")
                return True
        
        # Check for files without extension
        temp_files = os.listdir(os.path.dirname(output_path))
        base_name = os.path.basename(output_path)
        for file in temp_files:
            if file.startswith(base_name) and not file.endswith('.png'):
                print(f"Successfully downloaded (no extension): {file}")
                return True
        
        print("No audio file found after download")
        return False
        
    except Exception as e:
        print(f"Error downloading audio: {e}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def create_waveform_plot(audio_path, output_path):
    """
    Create a waveform visualization from audio file
    
    Args:
        audio_path (str): Path to the audio file
        output_path (str): Path where to save the waveform image
    
    Returns:
        dict: Information about the audio (duration, sample rate, etc.)
    """
    try:
        # Load audio file using librosa
        # sr=None means keep original sample rate
        # mono=True converts to mono if stereo
        y, sr = librosa.load(audio_path, sr=None, mono=True)
        
        # Calculate duration
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        
        # Create time axis
        time = np.linspace(0, duration, len(y))
        
        # Plot the waveform
        plt.plot(time, y, color='#667eea', linewidth=0.5, alpha=0.8)
        
        # Customize the plot
        plt.title('Audio Waveform', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time (seconds)', fontsize=12)
        plt.ylabel('Amplitude', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Set background color
        plt.gca().set_facecolor('#f8f9fa')
        plt.gcf().set_facecolor('white')
        
        # Add some styling
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        # Return audio information
        return {
            'duration': round(duration, 2),
            'sample_rate': sr,
            'samples': len(y),
            'max_amplitude': float(np.max(np.abs(y))),
            'rms_energy': float(np.sqrt(np.mean(y**2)))
        }
        
    except Exception as e:
        print(f"Error creating waveform: {e}")
        return None

@app.route('/')
def index():
    """
    Main page route - serves the HTML form
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """
    Handle form submission and process YouTube URL
    
    This route:
    1. Gets the YouTube URL from the form
    2. Downloads the audio
    3. Creates waveform visualization
    4. Returns results to the user
    """
    try:
        # Get YouTube URL from form
        youtube_url = request.form.get('youtube_url')
        
        if not youtube_url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400
        
        print(f"Processing YouTube URL: {youtube_url}")
        
        # Generate unique filenames for this request
        unique_id = str(uuid.uuid4())[:8]
        audio_filename = f"audio_{unique_id}"  # No extension, yt-dlp will add it
        waveform_filename = f"waveform_{unique_id}.png"
        
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        waveform_path = os.path.join(app.config['UPLOAD_FOLDER'], waveform_filename)
        
        print(f"Generated filenames - Audio: {audio_filename}, Waveform: {waveform_filename}")
        
        # Step 1: Download audio from YouTube
        print(f"Starting audio download from: {youtube_url}")
        if not download_youtube_audio(youtube_url, audio_path):
            print("Audio download failed")
            return jsonify({'error': 'Failed to download audio from YouTube. Please try again or check the URL.'}), 500
        
        # Find the actual downloaded file (yt-dlp may or may not add extension)
        actual_audio_path = None
        
        # First check for files with extensions
        for ext in ['.m4a', '.webm', '.mp3', '.wav']:
            test_path = audio_path + ext
            if os.path.exists(test_path):
                actual_audio_path = test_path
                print(f"Found downloaded audio file with extension: {actual_audio_path}")
                break
        
        # If no file with extension found, check for files without extension
        if not actual_audio_path:
            temp_files = os.listdir(app.config['UPLOAD_FOLDER'])
            print(f"Searching for files without extension. Available files: {temp_files}")
            # Look for files that start with our audio filename
            for file in temp_files:
                if file.startswith(os.path.basename(audio_path)) and not file.endswith('.png'):
                    actual_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
                    print(f"Found downloaded audio file without extension: {actual_audio_path}")
                    break
        
        if not actual_audio_path:
            # List files in temp_audio directory for debugging
            temp_files = os.listdir(app.config['UPLOAD_FOLDER'])
            print(f"Files in temp_audio directory: {temp_files}")
            return jsonify({'error': 'Downloaded audio file not found. Please try again.'}), 500
        
        # Step 2: Create waveform visualization
        print(f"Creating waveform visualization from: {actual_audio_path}")
        audio_info = create_waveform_plot(actual_audio_path, waveform_path)
        
        if not audio_info:
            print("Waveform creation failed")
            return jsonify({'error': 'Failed to create waveform visualization'}), 500
        
        print(f"Waveform created successfully: {waveform_path}")
        
        # Step 3: Clean up audio file (keep waveform for display)
        if os.path.exists(actual_audio_path):
            os.remove(actual_audio_path)
            print(f"Cleaned up audio file: {actual_audio_path}")
        
        # Return success response with waveform image and audio info
        return jsonify({
            'success': True,
            'waveform_image': f'/waveform/{waveform_filename}',
            'audio_info': audio_info,
            'youtube_url': youtube_url
        })
        
    except Exception as e:
        print(f"Error in analyze_audio: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/waveform/<filename>')
def serve_waveform(filename):
    """
    Serve waveform images to the browser
    """
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/health')
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Run the Flask app
    print("🎵 YouTube Audio Waveform Visualizer")
    print("=" * 40)
    print("Starting Flask server...")
    print(f"Host: {app.config['HOST']}")
    print(f"Port: {app.config['PORT']}")
    print(f"Debug: {app.config['DEBUG']}")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the server with configuration
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
