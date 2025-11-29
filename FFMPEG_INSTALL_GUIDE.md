# FFmpeg Installation Guide for Windows

## Why Do You Need FFmpeg?

FFmpeg is required for:
- **High Quality Video**: Merging separate video and audio streams for 1080p and higher
- **MP3 Conversion**: Converting audio to MP3 format
- **Best Quality**: Getting the highest quality downloads available

Without FFmpeg, the application will still work but with limitations:
- Videos download in lower quality (pre-merged formats)
- Audio downloads in original format (WebM, M4A, etc.)
- Some high-quality formats may not be available

## Quick Installation (Recommended)

### Option 1: Using Chocolatey (Easiest)

If you have Chocolatey package manager installed:

```cmd
choco install ffmpeg
```

### Option 2: Using Scoop

If you have Scoop package manager installed:

```cmd
scoop install ffmpeg
```

### Option 3: Manual Installation (Most Common)

1. **Download FFmpeg**
   - Go to: https://ffmpeg.org/download.html
   - Click on "Windows" builds
   - Choose a build provider (recommended: gyan.dev or BtbN)
   - Download the "ffmpeg-release-essentials.zip" or "ffmpeg-master-latest-win64-gpl.zip"

2. **Extract the Archive**
   - Extract the downloaded ZIP file
   - You'll get a folder like `ffmpeg-2024-11-29-git-xxxxx-essentials_build`
   - Inside, you'll find a `bin` folder containing `ffmpeg.exe`, `ffplay.exe`, and `ffprobe.exe`

3. **Add to System PATH**

   **Method A: Using System Properties (Permanent)**
   
   a. Copy the full path to the `bin` folder (e.g., `C:\ffmpeg\bin`)
   
   b. Open System Properties:
      - Press `Win + X` and select "System"
      - Click "Advanced system settings" on the right
      - Click "Environment Variables" button
   
   c. Edit PATH:
      - Under "System variables", find and select "Path"
      - Click "Edit"
      - Click "New"
      - Paste the path to the `bin` folder
      - Click "OK" on all windows
   
   d. Restart your command prompt or PowerShell

   **Method B: Quick Test (Temporary)**
   
   ```cmd
   set PATH=%PATH%;C:\path\to\ffmpeg\bin
   ```
   
   Replace `C:\path\to\ffmpeg\bin` with your actual path.

4. **Verify Installation**
   
   Open a new command prompt and run:
   ```cmd
   ffmpeg -version
   ```
   
   You should see FFmpeg version information.

## Detailed Step-by-Step with Screenshots

### Step 1: Download

1. Visit: https://www.gyan.dev/ffmpeg/builds/
2. Download: `ffmpeg-release-essentials.zip` (smaller, recommended)
   - Or download: `ffmpeg-release-full.zip` (includes extra features)

### Step 2: Extract

1. Right-click the downloaded ZIP file
2. Select "Extract All..."
3. Choose a location (recommended: `C:\ffmpeg`)
4. Click "Extract"

### Step 3: Locate the bin Folder

1. Navigate to the extracted folder
2. Open the folder (e.g., `ffmpeg-7.1-essentials_build`)
3. Find the `bin` folder inside
4. Copy the full path (e.g., `C:\ffmpeg\ffmpeg-7.1-essentials_build\bin`)

### Step 4: Add to PATH

1. Press `Win + R` to open Run dialog
2. Type `sysdm.cpl` and press Enter
3. Go to "Advanced" tab
4. Click "Environment Variables"
5. Under "System variables", find "Path"
6. Click "Edit"
7. Click "New"
8. Paste the path to the bin folder
9. Click "OK" three times to close all dialogs

### Step 5: Verify

1. Open a **new** Command Prompt (important: must be new)
2. Type: `ffmpeg -version`
3. You should see version information

## Troubleshooting

### "ffmpeg is not recognized..."

**Problem**: Command prompt doesn't recognize ffmpeg command.

**Solutions**:
1. Make sure you added the `bin` folder to PATH (not the parent folder)
2. Open a **new** command prompt (old ones won't see PATH changes)
3. Restart your computer if PATH changes don't take effect
4. Verify the path exists: `dir C:\path\to\ffmpeg\bin\ffmpeg.exe`

### "Access Denied" when editing PATH

**Problem**: You don't have administrator privileges.

**Solutions**:
1. Right-click Command Prompt and select "Run as administrator"
2. Or edit "User variables" PATH instead of "System variables"
3. Or ask your system administrator for help

### FFmpeg works in Command Prompt but not in the app

**Problem**: Application was running before FFmpeg was installed.

**Solutions**:
1. Close the YouTube Downloader application completely
2. Restart the application
3. The FFmpeg warning should no longer appear

### Downloads still fail with FFmpeg installed

**Problem**: Specific video format issues.

**Solutions**:
1. Try a different quality setting (720p instead of 1080p)
2. Check if the video is available in your region
3. Try downloading a different video to test
4. Check your internet connection

## Alternative: Portable FFmpeg

If you don't want to modify system PATH:

1. Download and extract FFmpeg as described above
2. Copy `ffmpeg.exe`, `ffplay.exe`, and `ffprobe.exe` from the `bin` folder
3. Paste them into the `yt_downloader` folder (same folder as `main.py`)
4. Restart the application

This works because the application checks the current directory for FFmpeg.

## Verifying FFmpeg in the Application

After installing FFmpeg:

1. Launch the YouTube Downloader
2. If FFmpeg is found, you won't see a warning
3. If you still see a warning, FFmpeg is not properly installed

## Getting Help

If you're still having trouble:

1. Open Command Prompt
2. Run: `where ffmpeg`
   - If it shows a path, FFmpeg is in PATH
   - If it says "not found", FFmpeg is not in PATH
3. Run: `echo %PATH%`
   - Check if your FFmpeg bin folder is listed

## Recommended FFmpeg Build

For most users, we recommend:
- **Provider**: gyan.dev
- **Build**: ffmpeg-release-essentials.zip
- **Size**: ~80 MB
- **Link**: https://www.gyan.dev/ffmpeg/builds/

This includes everything needed for the YouTube Downloader.

## Security Note

Always download FFmpeg from official sources:
- https://ffmpeg.org/download.html (official site)
- https://www.gyan.dev/ffmpeg/builds/ (trusted Windows builds)
- https://github.com/BtbN/FFmpeg-Builds/releases (trusted GitHub builds)

Never download FFmpeg from random websites or file-sharing sites.

## After Installation

Once FFmpeg is installed:
1. Restart the YouTube Downloader
2. You can now download:
   - 1080p and higher quality videos
   - MP3 audio files
   - Best available quality for all videos
3. The FFmpeg warning will no longer appear

Enjoy your enhanced downloading experience! 🎉
