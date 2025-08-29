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

# Create temporary folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def download_youtube_audio(url, output_path):
    """
    Download audio from YouTube URL using yt-dlp
    
    Args:
        url (str): YouTube video URL
        output_path (str): Path where to save the audio file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',  # Get best audio without conversion
            'outtmpl': output_path,      # Output template
            'quiet': False,  # Show progress for debugging
        }
        
        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
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
        
        # Generate unique filenames for this request
        unique_id = str(uuid.uuid4())[:8]
        audio_filename = f"audio_{unique_id}"  # No extension, yt-dlp will add it
        waveform_filename = f"waveform_{unique_id}.png"
        
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        waveform_path = os.path.join(app.config['UPLOAD_FOLDER'], waveform_filename)
        
        # Step 1: Download audio from YouTube
        print(f"Downloading audio from: {youtube_url}")
        if not download_youtube_audio(youtube_url, audio_path):
            return jsonify({'error': 'Failed to download audio from YouTube'}), 500
        
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
        print("Creating waveform visualization...")
        audio_info = create_waveform_plot(actual_audio_path, waveform_path)
        
        if not audio_info:
            return jsonify({'error': 'Failed to create waveform visualization'}), 500
        
        # Step 3: Clean up audio file (keep waveform for display)
        if os.path.exists(actual_audio_path):
            os.remove(actual_audio_path)
        
        # Return success response with waveform image and audio info
        return jsonify({
            'success': True,
            'waveform_image': f'/waveform/{waveform_filename}',
            'audio_info': audio_info,
            'youtube_url': youtube_url
        })
        
    except Exception as e:
        print(f"Error in analyze_audio: {e}")
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
    print("Open your browser and go to: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the development server
    app.run(debug=True, host='0.0.0.0', port=8000)
