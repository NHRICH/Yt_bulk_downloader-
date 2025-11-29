# YouTube Bulk Downloader - Usage Guide

## Quick Start

### 1. First Time Setup

Run the setup script to create the virtual environment and install dependencies:

```cmd
setup.bat
```

### 2. Launch the Application

Use the run script:

```cmd
run.bat
```

Or manually:

```cmd
venv\Scripts\activate.bat
python main.py
```

## Using the Application

### Step-by-Step Guide

1. **Enter YouTube URLs**
   - Paste one or more YouTube URLs in the text area
   - Each URL should be on a separate line
   - Supported formats:
     - `https://www.youtube.com/watch?v=VIDEO_ID`
     - `https://youtu.be/VIDEO_ID`
     - `https://www.youtube.com/shorts/VIDEO_ID`

2. **Select Format**
   - Click "Video (MP4)" for video downloads
   - Click "Audio Only (MP3)" for audio-only downloads
   - Note: Audio selection will disable the quality selector

3. **Choose Quality** (Video only)
   - Best Available: Highest quality available
   - 1080p: Full HD (requires FFmpeg)
   - 720p: HD
   - 480p: Standard definition

4. **Start Download**
   - Click the "Download" button
   - The button will be disabled during download
   - Watch the progress bar and status updates

5. **Monitor Progress**
   - Progress bar shows overall completion
   - Status label shows current file being downloaded
   - Example: "Downloading 2 of 5: Video Title..."

6. **Completion**
   - A popup will show download results
   - Files are saved in the `downloads` folder
   - The application is ready for the next batch

## Example Usage

### Downloading Multiple Videos

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=9bZkp7q19f0
https://youtu.be/jNQXAC9IVRw
```

1. Paste the URLs above into the text area
2. Select "Video (MP4)"
3. Choose "720p" quality
4. Click "Download"
5. Wait for completion

### Downloading Audio Only

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=9bZkp7q19f0
```

1. Paste the URLs above into the text area
2. Select "Audio Only (MP3)"
3. Click "Download"
4. Wait for completion

## Features

### Bulk Downloads
- Download multiple videos/audio files at once
- Process continues even if individual downloads fail
- Clear error reporting for failed downloads

### Format Options
- **Video (MP4)**: Download video with audio
- **Audio Only (MP3)**: Extract audio and convert to MP3

### Quality Selection
- **Best Available**: Automatically selects highest quality
- **1080p**: Full HD (requires FFmpeg for merging)
- **720p**: HD quality
- **480p**: Standard definition

### Real-time Feedback
- Progress bar shows overall completion percentage
- Status label shows current file and progress
- Non-blocking GUI stays responsive during downloads

### Error Handling
- Invalid URLs are detected before download starts
- Network errors are reported clearly
- Failed downloads don't stop the entire batch
- Completion popup shows success/failure summary

## File Organization

Downloaded files are automatically saved to:
```
yt_downloader/downloads/
```

Files are named using the video title with invalid characters removed.

## FFmpeg Requirement

FFmpeg is required for:
- 1080p video downloads (merging video and audio streams)
- MP3 audio conversion

### Installing FFmpeg

1. Download from: https://ffmpeg.org/download.html
2. Extract the archive
3. Add the `bin` folder to your system PATH
4. Restart the application

### Checking FFmpeg Installation

```cmd
ffmpeg -version
```

If FFmpeg is not found, the application will show a warning on startup.

## Troubleshooting

### "No URLs provided" Error
- Make sure you've entered at least one URL
- Check that URLs are not empty lines

### "Invalid URLs found" Error
- Verify the URLs are from YouTube
- Check for typos in the URLs
- Ensure URLs are complete (include https://)

### Download Fails
- Check your internet connection
- Verify the video is available (not private/deleted)
- Some videos may be region-restricted
- Age-restricted videos may require authentication

### GUI Freezes
- The application uses threading to prevent freezing
- If it still freezes, try downloading fewer videos at once
- Check system resources (CPU, memory, disk space)

### FFmpeg Warning
- Install FFmpeg to enable 1080p and MP3 features
- Lower quality videos (720p, 480p) work without FFmpeg
- Video format downloads work without FFmpeg (except 1080p)

## Tips

1. **Test with one URL first** before bulk downloading
2. **Use "Best Available"** if you're unsure about quality
3. **Check disk space** before downloading many videos
4. **Close other applications** if downloads are slow
5. **Use audio-only** to save bandwidth and storage

## Keyboard Shortcuts

- **Ctrl+A**: Select all text in URL input
- **Ctrl+C**: Copy selected text
- **Ctrl+V**: Paste text
- **Ctrl+X**: Cut selected text

## Advanced Usage

### Running Tests

To verify the application is working correctly:

```cmd
venv\Scripts\activate.bat
pytest test_downloader.py -v
```

### Checking Logs

The application prints download progress to the console when run manually:

```cmd
venv\Scripts\activate.bat
python main.py
```

## Support

For issues or questions:
1. Check this usage guide
2. Review the README.md file
3. Check the troubleshooting section
4. Verify FFmpeg installation
5. Test with a single, known-working YouTube URL

## License

This application is for educational and personal use only.
