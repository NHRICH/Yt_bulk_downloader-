"""
YouTube Bulk Downloader
A modern GUI application for downloading multiple YouTube videos or audio files.
"""

import os
import re
import threading
import shutil
from typing import Callable, Optional
from dataclasses import dataclass
import customtkinter as ctk
import yt_dlp


@dataclass
class DownloadResult:
    """Result of a single download operation."""
    url: str
    success: bool
    message: str
    filename: Optional[str] = None


class DownloaderEngine:
    """Handles YouTube download operations using yt-dlp."""
    
    def __init__(self, download_dir: str) -> None:
        """
        Initialize the downloader engine.
        
        Args:
            download_dir: Directory where downloads will be saved
        """
        self.download_dir = download_dir
        self.current_index = 0
        self.total_urls = 0
        self.progress_callback: Optional[Callable[[int, int, str], None]] = None
        
        # Create downloads directory if it doesn't exist
        os.makedirs(self.download_dir, exist_ok=True)
    
    def check_ffmpeg(self) -> bool:
        """
        Check if FFmpeg is available in the system PATH.
        
        Returns:
            True if FFmpeg is available, False otherwise
        """
        return shutil.which("ffmpeg") is not None
    
    def validate_urls(self, urls: list[str]) -> tuple[list[str], list[str]]:
        """
        Validate YouTube URLs.
        
        Args:
            urls: List of URLs to validate
            
        Returns:
            Tuple of (valid_urls, invalid_urls)
        """
        youtube_pattern = re.compile(
            r'(https?://)?(www\.)?(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)[a-zA-Z0-9_-]+'
        )
        
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            url = url.strip()
            if not url:
                continue
            if youtube_pattern.match(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        return valid_urls, invalid_urls
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename by removing invalid characters.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename safe for filesystem
        """
        # Remove invalid characters
        invalid_chars = r'[<>:"/\\|?*]'
        sanitized = re.sub(invalid_chars, '_', filename)
        
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip('. ')
        
        # Remove underscores if that's all that's left
        if sanitized.replace('_', '').strip() == '':
            sanitized = "download"
        
        # Ensure filename is not empty
        if not sanitized:
            sanitized = "download"
        
        return sanitized
    
    def get_ydl_opts(self, format_type: str, quality: str) -> dict:
        """
        Build yt-dlp options based on format and quality selection.
        
        Args:
            format_type: "video" or "audio"
            quality: "best", "1080p", "720p", or "480p"
            
        Returns:
            Dictionary of yt-dlp options
        """
        base_opts = {
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': False,
            'no_warnings': False,
        }
        
        # Check if FFmpeg is available
        has_ffmpeg = self.check_ffmpeg()
        
        if format_type == "audio":
            if has_ffmpeg:
                base_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                # Without FFmpeg, download best audio format available
                base_opts.update({
                    'format': 'bestaudio/best',
                })
        else:  # video
            if has_ffmpeg:
                # With FFmpeg, we can merge video and audio
                if quality == "Best Available":
                    base_opts['format'] = 'bestvideo+bestaudio/best'
                else:
                    height = quality.rstrip('p')
                    base_opts['format'] = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
            else:
                # Without FFmpeg, use pre-merged formats only
                if quality == "Best Available":
                    base_opts['format'] = 'best'
                else:
                    height = quality.rstrip('p')
                    # Try to get a pre-merged format at the requested quality
                    base_opts['format'] = f'best[height<={height}]/best'
        
        return base_opts
    
    def progress_hook(self, d: dict) -> None:
        """
        Progress hook called by yt-dlp during download.
        
        Args:
            d: Progress dictionary from yt-dlp
        """
        if d['status'] == 'downloading' and self.progress_callback:
            # Extract progress information
            if 'filename' in d:
                filename = os.path.basename(d['filename'])
                title = filename
            else:
                title = "Unknown"
            
            # Call the progress callback
            self.progress_callback(self.current_index, self.total_urls, title)
    
    def download_videos(
        self,
        urls: list[str],
        format_type: str,
        quality: str,
        progress_callback: Callable[[int, int, str], None]
    ) -> list[DownloadResult]:
        """
        Download multiple videos/audio files.
        
        Args:
            urls: List of YouTube URLs to download
            format_type: "video" or "audio"
            quality: Quality selection
            progress_callback: Callback function for progress updates
            
        Returns:
            List of DownloadResult objects
        """
        self.progress_callback = progress_callback
        self.total_urls = len(urls)
        results = []
        
        ydl_opts = self.get_ydl_opts(format_type, quality)
        
        for index, url in enumerate(urls, 1):
            self.current_index = index
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'Unknown')
                    
                    results.append(DownloadResult(
                        url=url,
                        success=True,
                        message=f"Successfully downloaded: {title}",
                        filename=title
                    ))
            except Exception as e:
                results.append(DownloadResult(
                    url=url,
                    success=False,
                    message=f"Failed to download {url}: {str(e)}"
                ))
        
        return results


class App(ctk.CTk):
    """Main application GUI."""
    
    def __init__(self) -> None:
        """Initialize the application."""
        super().__init__()
        
        # Configure window
        self.title("YouTube Bulk Downloader")
        self.geometry("700x600")
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize downloader engine
        download_dir = os.path.join(os.path.dirname(__file__), "downloads")
        self.engine = DownloaderEngine(download_dir)
        
        # Setup UI
        self.setup_ui()
        
        # Check FFmpeg on startup
        self.check_ffmpeg_availability()
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Title label
        title_label = ctk.CTkLabel(
            self,
            text="YouTube Bulk Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # URL input label
        url_label = ctk.CTkLabel(
            self,
            text="Enter YouTube URLs (one per line):",
            font=ctk.CTkFont(size=14)
        )
        url_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")
        
        # URL input textbox
        self.url_textbox = ctk.CTkTextbox(
            self,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        self.url_textbox.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        # Format selection label
        format_label = ctk.CTkLabel(
            self,
            text="Format:",
            font=ctk.CTkFont(size=14)
        )
        format_label.grid(row=3, column=0, padx=20, pady=(15, 5), sticky="w")
        
        # Format selector
        self.format_selector = ctk.CTkSegmentedButton(
            self,
            values=["Video (MP4)", "Audio Only (MP3)"],
            command=self.on_format_change
        )
        self.format_selector.set("Video (MP4)")
        self.format_selector.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # Quality selection label
        quality_label = ctk.CTkLabel(
            self,
            text="Quality:",
            font=ctk.CTkFont(size=14)
        )
        quality_label.grid(row=5, column=0, padx=20, pady=(15, 5), sticky="w")
        
        # Quality selector
        self.quality_selector = ctk.CTkComboBox(
            self,
            values=["Best Available", "1080p", "720p", "480p"],
            state="readonly"
        )
        self.quality_selector.set("Best Available")
        self.quality_selector.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        
        # Download button
        self.download_button = ctk.CTkButton(
            self,
            text="Download",
            command=self.start_download,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.download_button.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=8, column=0, padx=20, pady=5, sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=9, column=0, padx=20, pady=5, sticky="w")
    
    def on_format_change(self, value: str) -> None:
        """
        Handle format selection change.
        
        Args:
            value: Selected format value
        """
        if value == "Audio Only (MP3)":
            self.quality_selector.configure(state="disabled")
        else:
            self.quality_selector.configure(state="readonly")
    
    def check_ffmpeg_availability(self) -> None:
        """Check if FFmpeg is available and warn if not."""
        if not self.engine.check_ffmpeg():
            self.show_warning(
                "FFmpeg Not Found",
                "FFmpeg is not installed or not in your system PATH.\n\n"
                "Without FFmpeg:\n"
                "- Videos will download in lower quality (pre-merged formats)\n"
                "- Audio downloads will be in original format (not MP3)\n"
                "- High quality downloads may not be available\n\n"
                "To get the best quality:\n"
                "1. Download FFmpeg from: https://ffmpeg.org/download.html\n"
                "2. Add it to your system PATH\n"
                "3. Restart this application\n\n"
                "The application will continue to work with reduced quality."
            )
    
    def start_download(self) -> None:
        """Start the download process."""
        # Get URLs from textbox
        url_text = self.url_textbox.get("1.0", "end-1c")
        urls = [url.strip() for url in url_text.split('\n') if url.strip()]
        
        # Validate input
        if not urls:
            self.show_error("No URLs provided. Please enter at least one YouTube URL.")
            return
        
        # Validate URLs
        valid_urls, invalid_urls = self.engine.validate_urls(urls)
        
        if invalid_urls:
            self.show_error(
                f"Invalid URLs found:\n" + "\n".join(invalid_urls[:5]) +
                (f"\n... and {len(invalid_urls) - 5} more" if len(invalid_urls) > 5 else "")
            )
            return
        
        if not valid_urls:
            self.show_error("No valid YouTube URLs found.")
            return
        
        # Get format and quality
        format_type = "audio" if self.format_selector.get() == "Audio Only (MP3)" else "video"
        quality = self.quality_selector.get()
        
        # Check FFmpeg and warn if needed for high quality
        if not self.engine.check_ffmpeg():
            if format_type == "audio":
                self.show_info(
                    "Note: FFmpeg Not Available",
                    "Audio will be downloaded in original format (not MP3).\n"
                    "Install FFmpeg for MP3 conversion."
                )
            elif quality in ["Best Available", "1080p"]:
                self.show_info(
                    "Note: FFmpeg Not Available",
                    f"Video will download in lower quality (pre-merged format).\n"
                    "Install FFmpeg for best quality downloads."
                )
        
        # Disable download button
        self.download_button.configure(state="disabled")
        self.status_label.configure(text="Starting download...")
        self.progress_bar.set(0)
        
        # Start download in separate thread
        thread = threading.Thread(
            target=self.download_thread_worker,
            args=(valid_urls, format_type, quality),
            daemon=True
        )
        thread.start()
    
    def download_thread_worker(self, urls: list[str], format_type: str, quality: str) -> None:
        """
        Worker thread for downloading videos.
        
        Args:
            urls: List of URLs to download
            format_type: "video" or "audio"
            quality: Quality selection
        """
        try:
            results = self.engine.download_videos(
                urls,
                format_type,
                quality,
                self.update_progress
            )
            
            # Update GUI on main thread
            self.after(0, self.on_download_complete, results)
        except Exception as e:
            self.after(0, self.show_error, f"Download error: {str(e)}")
        finally:
            self.after(0, lambda: self.download_button.configure(state="normal"))
    
    def update_progress(self, current: int, total: int, title: str) -> None:
        """
        Update progress indicators.
        
        Args:
            current: Current download index
            total: Total number of downloads
            title: Title of current download
        """
        # Calculate progress
        progress = current / total if total > 0 else 0
        
        # Update GUI on main thread
        self.after(0, lambda: self.progress_bar.set(progress))
        self.after(0, lambda: self.status_label.configure(
            text=f"Downloading {current} of {total}: {title[:50]}..."
        ))
    
    def on_download_complete(self, results: list[DownloadResult]) -> None:
        """
        Handle download completion.
        
        Args:
            results: List of download results
        """
        # Count successes and failures
        successes = sum(1 for r in results if r.success)
        failures = len(results) - successes
        
        # Update status
        self.status_label.configure(text="Download Complete!")
        self.progress_bar.set(1.0)
        
        # Show completion message
        message = f"Download complete!\n\nSuccessful: {successes}\nFailed: {failures}"
        
        if failures > 0:
            failed_urls = [r.url for r in results if not r.success]
            message += f"\n\nFailed URLs:\n" + "\n".join(failed_urls[:3])
            if len(failed_urls) > 3:
                message += f"\n... and {len(failed_urls) - 3} more"
        
        self.show_info("Download Complete", message)
    
    def show_error(self, message: str) -> None:
        """
        Show error message dialog.
        
        Args:
            message: Error message to display
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=350,
            font=ctk.CTkFont(size=12)
        )
        label.pack(padx=20, pady=20)
        
        button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        )
        button.pack(pady=10)
    
    def show_warning(self, title: str, message: str) -> None:
        """
        Show warning message dialog.
        
        Args:
            title: Dialog title
            message: Warning message to display
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("450x250")
        dialog.transient(self)
        
        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=400,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        label.pack(padx=20, pady=20)
        
        button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        )
        button.pack(pady=10)
    
    def show_info(self, title: str, message: str) -> None:
        """
        Show info message dialog.
        
        Args:
            title: Dialog title
            message: Info message to display
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=350,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        label.pack(padx=20, pady=20)
        
        button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        )
        button.pack(pady=10)


def main() -> None:
    """Main entry point."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
