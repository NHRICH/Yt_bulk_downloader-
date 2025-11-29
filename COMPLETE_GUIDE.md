# YouTube Bulk Downloader - Complete Guide

## 🎉 Welcome!

You now have a fully functional YouTube Bulk Downloader with a modern GUI. This guide will help you get started quickly.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [First Time Setup](#first-time-setup)
3. [Using the Application](#using-the-application)
4. [Understanding FFmpeg](#understanding-ffmpeg)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)

---

## 🚀 Quick Start

### Absolute Fastest Way to Start

```cmd
cd yt_downloader
setup.bat
run.bat
```

That's it! The application will open and you can start downloading.

---

## 🔧 First Time Setup

### Step 1: Run Setup Script

Open Command Prompt in the `yt_downloader` folder and run:

```cmd
setup.bat
```

This will:
- Create a Python virtual environment
- Install all required packages (customtkinter, yt-dlp, pytest, hypothesis)
- Take about 1-2 minutes

### Step 2: Launch the Application

```cmd
run.bat
```

The GUI will open immediately!

### Step 3: (Optional) Install FFmpeg

You'll see a warning about FFmpeg. You can:
- **Option A**: Ignore it and use the app with reduced quality
- **Option B**: Install FFmpeg for best quality (see `FFMPEG_INSTALL_GUIDE.md`)

---

## 💻 Using the Application

### Basic Usage

1. **Paste URLs**
   - Copy YouTube video URLs
   - Paste them in the text area (one per line)
   - Example:
     ```
     https://www.youtube.com/watch?v=dQw4w9WgXcQ
     https://youtu.be/9bZkp7q19f0
     ```

2. **Choose Format**
   - Click "Video (MP4)" for video files
   - Click "Audio Only (MP3)" for audio files

3. **Select Quality** (Video only)
   - Best Available (recommended)
   - 1080p (requires FFmpeg)
   - 720p
   - 480p

4. **Click Download**
   - Watch the progress bar
   - See status updates
   - Wait for completion popup

5. **Find Your Files**
   - Open the `downloads` folder
   - Your files are there!

### Example: Download 3 Videos

```
1. Paste these URLs:
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   https://www.youtube.com/watch?v=9bZkp7q19f0
   https://youtu.be/jNQXAC9IVRw

2. Select "Video (MP4)"

3. Choose "720p"

4. Click "Download"

5. Wait for "Download Complete!" popup

6. Check the downloads folder
```

---

## 🎬 Understanding FFmpeg

### What is FFmpeg?

FFmpeg is a free tool that helps process video and audio files.

### Do You Need It?

**No, but it's recommended.**

### Without FFmpeg

✅ Application works fine
✅ Downloads videos successfully
⚠️ Lower quality (usually 720p max)
⚠️ Audio in original format (not MP3)

### With FFmpeg

✅ Best quality available
✅ 1080p and higher
✅ MP3 audio conversion
✅ All features unlocked

### How to Install FFmpeg

See the detailed guide: `FFMPEG_INSTALL_GUIDE.md`

**Quick version:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Restart the application

---

## 🔍 Troubleshooting

### "No URLs provided"

**Problem**: You clicked Download without entering URLs.

**Solution**: Paste at least one YouTube URL in the text area.

---

### "Invalid URLs found"

**Problem**: Some URLs are not from YouTube.

**Solution**: 
- Make sure URLs start with `https://youtube.com` or `https://youtu.be`
- Check for typos
- Remove non-YouTube URLs

---

### Download Fails

**Problem**: Download starts but fails with an error.

**Possible Causes & Solutions**:

1. **No Internet Connection**
   - Check your internet
   - Try opening YouTube in a browser

2. **Video Not Available**
   - Video might be private or deleted
   - Try a different video

3. **Region Restricted**
   - Video not available in your country
   - Try a different video

4. **Age Restricted**
   - Some videos require authentication
   - Try a different video

---

### GUI Freezes

**Problem**: Application becomes unresponsive.

**Solution**:
- This shouldn't happen (we use threading)
- If it does, close and restart the application
- Try downloading fewer videos at once

---

### FFmpeg Warning Keeps Appearing

**Problem**: You installed FFmpeg but still see the warning.

**Solution**:
1. Close the application completely
2. Open Command Prompt
3. Type: `ffmpeg -version`
4. If it works, restart the application
5. If it doesn't work, FFmpeg is not in PATH

---

### Downloads Are Slow

**Problem**: Downloads take a long time.

**Possible Causes**:
- Slow internet connection (most common)
- Large video files
- YouTube server speed

**Not a Problem With**:
- The application (it's as fast as your internet)

---

## 🎓 Advanced Usage

### Running Tests

Verify everything works:

```cmd
venv\Scripts\activate.bat
pytest test_downloader.py -v
```

You should see: `14 passed`

---

### Manual Launch

Instead of using `run.bat`:

```cmd
venv\Scripts\activate.bat
python main.py
```

---

### Checking FFmpeg Status

```cmd
ffmpeg -version
```

If installed, you'll see version information.

---

### Cleaning Up

To remove downloaded files:

```cmd
rmdir /s /q downloads
```

The folder will be recreated automatically next time.

---

### Updating Dependencies

```cmd
venv\Scripts\activate.bat
pip install --upgrade customtkinter yt-dlp
```

---

## 📁 File Locations

```
yt_downloader/
├── main.py                    # The application
├── run.bat                    # Quick launch
├── setup.bat                  # First-time setup
├── downloads/                 # Your downloaded files
└── venv/                      # Python environment
```

---

## 🎯 Tips & Tricks

### Tip 1: Test First
Always test with one URL before bulk downloading.

### Tip 2: Use Best Available
Unless you have a specific need, use "Best Available" quality.

### Tip 3: Audio for Music
Use "Audio Only (MP3)" for music videos to save space.

### Tip 4: Check Disk Space
Make sure you have enough disk space before downloading many videos.

### Tip 5: Close Other Apps
Close bandwidth-heavy apps for faster downloads.

---

## 📚 Additional Documentation

- `README.md` - Project overview
- `USAGE_GUIDE.md` - Detailed usage instructions
- `FFMPEG_INSTALL_GUIDE.md` - FFmpeg installation
- `PROJECT_SUMMARY.md` - Technical details
- `STATUS.md` - Current status and features

---

## ❓ FAQ

### Q: Is this legal?
A: Downloading videos for personal use is generally acceptable. Respect copyright and YouTube's terms of service.

### Q: Can I download playlists?
A: No, paste individual video URLs only.

### Q: Can I pause downloads?
A: No, but you can close the application and restart.

### Q: Where are files saved?
A: In the `downloads` folder inside `yt_downloader`.

### Q: Can I change the download location?
A: Not currently, files always go to the `downloads` folder.

### Q: Does this work on Mac/Linux?
A: It should work with minor modifications to the setup scripts.

### Q: How do I update the application?
A: Replace `main.py` with a newer version and restart.

### Q: Can I download age-restricted videos?
A: Not currently, the application doesn't handle authentication.

---

## 🎉 You're Ready!

You now know everything you need to use the YouTube Bulk Downloader.

### Quick Recap

1. Run `setup.bat` (first time only)
2. Run `run.bat` (every time)
3. Paste URLs
4. Choose format and quality
5. Click Download
6. Find files in `downloads` folder

### For Best Experience

Install FFmpeg following `FFMPEG_INSTALL_GUIDE.md`

---

## 🆘 Still Need Help?

1. Check `USAGE_GUIDE.md` for detailed instructions
2. Check `FFMPEG_INSTALL_GUIDE.md` for FFmpeg help
3. Run tests: `pytest test_downloader.py -v`
4. Check `STATUS.md` for current features

---

## 🎊 Enjoy!

Happy downloading! 🎥🎵

---

**Made with ❤️ using Python, CustomTkinter, and yt-dlp**
