# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Flask web application
- YouTube audio extraction with yt-dlp
- Waveform visualization with matplotlib
- Beautiful responsive web interface
- Audio analysis and statistics
- Error handling and validation
- Docker support
- Development tools (Makefile, linting, testing)

### Changed
- Fixed FFmpeg dependency issue by removing post-processing step
- Updated yt-dlp configuration to work without FFmpeg

### Fixed
- Port conflict with AirPlay on macOS (changed from 5000 to 8000)
- Audio file extension handling for different formats

## [1.0.0] - 2025-08-30

### Added
- Initial release
- Core functionality for YouTube audio waveform visualization
- Web interface with modern design
- Audio processing with librosa
- Real-time waveform generation
- Audio statistics display
- Example YouTube URLs for testing
- Comprehensive documentation
- MIT License
- Professional project structure

### Features
- Extract audio from any YouTube video
- Generate beautiful waveform visualizations
- Display audio statistics (duration, sample rate, amplitude, etc.)
- Responsive web design
- Error handling and user feedback
- Mobile-friendly interface
- Fast processing with optimized libraries

### Technical Details
- Flask web framework
- yt-dlp for YouTube video processing
- librosa for audio analysis
- matplotlib for visualization
- Modern HTML/CSS/JavaScript frontend
- Docker containerization
- Development tools and linting
