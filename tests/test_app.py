#!/usr/bin/env python3
"""
Tests for the YouTube Audio Waveform Visualizer Flask application
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from app import app, download_youtube_audio, create_waveform_plot


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test that the index route returns 200 and contains expected content"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'YouTube Audio Waveform Visualizer' in response.data
    assert b'Analyze Audio' in response.data


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_analyze_audio_missing_url(client):
    """Test analyze endpoint with missing URL"""
    response = client.post('/analyze', data={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Please provide a YouTube URL' in data['error']


@patch('app.download_youtube_audio')
@patch('app.create_waveform_plot')
def test_analyze_audio_success(mock_create_waveform, mock_download, client):
    """Test successful audio analysis"""
    # Mock successful download
    mock_download.return_value = True
    
    # Mock waveform creation
    mock_create_waveform.return_value = {
        'duration': 120.5,
        'sample_rate': 44100,
        'samples': 5313600,
        'max_amplitude': 0.8,
        'rms_energy': 0.3
    }
    
    # Mock file existence
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        
        response = client.post('/analyze', data={
            'youtube_url': 'https://www.youtube.com/watch?v=test'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'waveform_image' in data
        assert 'audio_info' in data


@patch('app.download_youtube_audio')
def test_analyze_audio_download_failure(mock_download, client):
    """Test audio analysis when download fails"""
    mock_download.return_value = False
    
    response = client.post('/analyze', data={
        'youtube_url': 'https://www.youtube.com/watch?v=test'
    })
    
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Failed to download audio' in data['error']


def test_waveform_route_not_found(client):
    """Test waveform route with non-existent file"""
    response = client.get('/waveform/nonexistent.png')
    assert response.status_code == 404


def test_download_youtube_audio_success():
    """Test successful YouTube audio download"""
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance
        
        result = download_youtube_audio('https://www.youtube.com/watch?v=test', 'test.mp3')
        
        assert result is True
        mock_instance.download.assert_called_once()


def test_download_youtube_audio_failure():
    """Test YouTube audio download failure"""
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_ydl.side_effect = Exception("Download failed")
        
        result = download_youtube_audio('https://www.youtube.com/watch?v=test', 'test.mp3')
        
        assert result is False


@patch('librosa.load')
@patch('matplotlib.pyplot')
def test_create_waveform_plot_success(mock_plt, mock_load):
    """Test successful waveform plot creation"""
    # Mock librosa load
    mock_load.return_value = ([0.1, 0.2, 0.3], 44100)
    
    # Mock matplotlib
    mock_fig = MagicMock()
    mock_plt.figure.return_value = mock_fig
    mock_plt.linspace.return_value = [0, 1, 2]
    
    with tempfile.NamedTemporaryFile(suffix='.png') as tmp_file:
        result = create_waveform_plot('test.mp3', tmp_file.name)
        
        assert result is not None
        assert 'duration' in result
        assert 'sample_rate' in result
        assert 'samples' in result


@patch('librosa.load')
def test_create_waveform_plot_failure(mock_load):
    """Test waveform plot creation failure"""
    mock_load.side_effect = Exception("Audio processing failed")
    
    with tempfile.NamedTemporaryFile(suffix='.png') as tmp_file:
        result = create_waveform_plot('test.mp3', tmp_file.name)
        
        assert result is None


if __name__ == '__main__':
    pytest.main([__file__])
