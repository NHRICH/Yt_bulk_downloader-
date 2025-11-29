# YouTube Bulk Downloader

A modern, threaded YouTube downloader with a clean GUI built using CustomTkinter and yt-dlp.

## Features

- **Bulk Downloads**: Download multiple YouTube videos or audio files at once
- **Format Selection**: Choose between Video (MP4) or Audio Only (MP3)
- **Quality Control**: Select video quality (Best, 1080p, 720p, 480p)
- **Real-time Progress**: Live progress bar and status updates
- **Threaded Downloads**: Non-blocking GUI that stays responsive
- **Modern UI**: Dark mode interface with CustomTkinter
- **Error Handling**: Comprehensive error messages and validation

## Requirements

- Python 3.10 or higher
- FFmpeg (required for 1080p video merging and MP3 conversion)

## Installation

### 1. Run Setup Script

```cmd
setup.bat
```

This will:
- Create a virtual environment
- Install all required dependencies

### 2. Install FFmpeg (Recommended)

FFmpeg is recommended for best quality downloads and MP3 conversion.

**Quick Install:**
- See detailed instructions in `FFMPEG_INSTALL_GUIDE.md`
- Or download from: https://ffmpeg.org/download.html

**Note:** The application works without FFmpeg but with reduced quality.

**Windows Installation:**
1. Download the FFmpeg build for Windows
2. Extract the archive
3. Add the `bin` folder to your system PATH
4. Verify installation: `ffmpeg -version`

For detailed step-by-step instructions, see `FFMPEG_INSTALL_GUIDE.md`

## Usage

### Quick Start

```cmd
run.bat
```

Or manually:

```cmd
venv\Scripts\activate.bat
python main.py
```

### How to Use

1. **Enter URLs**: Paste YouTube URLs in the text area (one per line)
2. **Select Format**: Choose Video (MP4) or Audio Only (MP3)
3. **Select Quality**: Choose video quality (disabled for audio)
4. **Click Download**: Start the download process
5. **Monitor Progress**: Watch the progress bar and status updates

### Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`

## File Structure

```
yt_downloader/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── setup.bat           # Setup script
├── run.bat             # Run script
├── README.md           # This file
├── venv/               # Virtual environment (created by setup)
└── downloads/          # Downloaded files (created automatically)
```

## Dependencies

- **customtkinter**: Modern UI framework
- **yt-dlp**: YouTube download engine
- **pytest**: Testing framework
- **hypothesis**: Property-based testing

## Troubleshooting

### FFmpeg Not Found

If you see a warning about FFmpeg:
- Make sure FFmpeg is installed
- Verify it's in your system PATH
- Restart the application after installation

### Download Fails

- Check your internet connection
- Verify the YouTube URL is valid
- Some videos may be restricted or unavailable

### GUI Freezes

The application uses threading to prevent freezing. If it still freezes:
- Check if you have enough system resources
- Try downloading fewer videos at once

## Development

### Running Tests

```cmd
venv\Scripts\activate.bat
pytest
```

### Project Structure

- `DownloaderEngine`: Handles download logic and yt-dlp integration
- `App`: Main GUI application class
- Threading model ensures responsive UI during downloads

## License

This project is for educational purposes.

## Credits

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
