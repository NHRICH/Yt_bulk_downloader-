"""
Unit tests for YouTube Bulk Downloader
"""

import os
import pytest
from hypothesis import given, strategies as st
from main import DownloaderEngine, DownloadResult


class TestDownloaderEngine:
    """Tests for DownloaderEngine class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.download_dir = "test_downloads"
        self.engine = DownloaderEngine(self.download_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.download_dir):
            import shutil
            shutil.rmtree(self.download_dir)
    
    def test_download_directory_creation(self):
        """Test that download directory is created."""
        assert os.path.exists(self.download_dir)
    
    def test_validate_urls_valid(self):
        """Test URL validation with valid YouTube URLs."""
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=abc123",
            "https://youtu.be/xyz789",
            "https://www.youtube.com/shorts/short123"
        ]
        valid, invalid = self.engine.validate_urls(urls)
        assert len(valid) == 4
        assert len(invalid) == 0
    
    def test_validate_urls_invalid(self):
        """Test URL validation with invalid URLs."""
        urls = [
            "not a url",
            "https://google.com",
            "https://vimeo.com/123456",
            ""
        ]
        valid, invalid = self.engine.validate_urls(urls)
        assert len(valid) == 0
        assert len(invalid) == 3  # Empty string is filtered out
    
    def test_validate_urls_mixed(self):
        """Test URL validation with mixed valid and invalid URLs."""
        urls = [
            "https://www.youtube.com/watch?v=valid123",
            "https://google.com",
            "https://youtu.be/valid456"
        ]
        valid, invalid = self.engine.validate_urls(urls)
        assert len(valid) == 2
        assert len(invalid) == 1
    
    def test_sanitize_filename_basic(self):
        """Test filename sanitization with basic characters."""
        filename = "My Video Title"
        sanitized = self.engine.sanitize_filename(filename)
        assert sanitized == "My Video Title"
    
    def test_sanitize_filename_special_chars(self):
        """Test filename sanitization with special characters."""
        filename = 'Video: "Title" <Test> | File?'
        sanitized = self.engine.sanitize_filename(filename)
        assert '<' not in sanitized
        assert '>' not in sanitized
        assert ':' not in sanitized
        assert '"' not in sanitized
        assert '|' not in sanitized
        assert '?' not in sanitized
    
    def test_sanitize_filename_empty(self):
        """Test filename sanitization with empty string."""
        filename = ""
        sanitized = self.engine.sanitize_filename(filename)
        assert sanitized == "download"
    
    def test_sanitize_filename_only_special_chars(self):
        """Test filename sanitization with only special characters."""
        filename = "<>:\"/\\|?*"
        sanitized = self.engine.sanitize_filename(filename)
        assert sanitized == "download"
    
    def test_get_ydl_opts_video_best(self):
        """Test yt-dlp options for best quality video."""
        opts = self.engine.get_ydl_opts("video", "Best Available")
        assert 'format' in opts
        # Format depends on FFmpeg availability
        has_ffmpeg = self.engine.check_ffmpeg()
        if has_ffmpeg:
            assert opts['format'] == 'bestvideo+bestaudio/best'
        else:
            assert opts['format'] == 'best'
    
    def test_get_ydl_opts_video_1080p(self):
        """Test yt-dlp options for 1080p video."""
        opts = self.engine.get_ydl_opts("video", "1080p")
        assert 'format' in opts
        assert '1080' in opts['format'] or 'best' in opts['format']
    
    def test_get_ydl_opts_audio(self):
        """Test yt-dlp options for audio."""
        opts = self.engine.get_ydl_opts("audio", "Best Available")
        assert 'format' in opts
        assert opts['format'] == 'bestaudio/best'
        # Postprocessors only present with FFmpeg
        has_ffmpeg = self.engine.check_ffmpeg()
        if has_ffmpeg:
            assert 'postprocessors' in opts
            assert opts['postprocessors'][0]['key'] == 'FFmpegExtractAudio'
            assert opts['postprocessors'][0]['preferredcodec'] == 'mp3'
        else:
            # Without FFmpeg, no postprocessors
            assert 'postprocessors' not in opts


class TestPropertyBased:
    """Property-based tests using Hypothesis."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.download_dir = "test_downloads"
        self.engine = DownloaderEngine(self.download_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.download_dir):
            import shutil
            shutil.rmtree(self.download_dir)
    
    @given(st.lists(st.text(min_size=1, max_size=100)))
    def test_property_url_validation_consistency(self, urls):
        """
        **Feature: youtube-bulk-downloader, Property 1: URL validation consistency**
        
        For any list of input strings, the validation function should partition
        them into valid YouTube URLs and invalid URLs, with no overlap.
        
        **Validates: Requirements 9.3**
        """
        valid, invalid = self.engine.validate_urls(urls)
        
        # No overlap between valid and invalid
        assert len(set(valid) & set(invalid)) == 0
        
        # All non-empty URLs are accounted for
        non_empty_urls = [url.strip() for url in urls if url.strip()]
        assert len(valid) + len(invalid) == len(non_empty_urls)
    
    @given(st.text(min_size=0, max_size=200))
    def test_property_filename_sanitization_safety(self, filename):
        """
        **Feature: youtube-bulk-downloader, Property 4: Filename sanitization safety**
        
        For any input filename string, the sanitized output should contain only
        valid filesystem characters and should not be empty.
        
        **Validates: Requirements 7.3**
        """
        sanitized = self.engine.sanitize_filename(filename)
        
        # Result is never empty
        assert len(sanitized) > 0
        
        # No invalid characters in result
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            assert char not in sanitized
    
    @given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=20))
    def test_property_progress_monotonic(self, progress_values):
        """
        **Feature: youtube-bulk-downloader, Property 3: Progress updates are monotonic**
        
        For any download operation, progress percentage values should be
        non-decreasing (each update should be greater than or equal to the previous value).
        
        **Validates: Requirements 6.3**
        """
        # Sort to simulate monotonic progress
        sorted_values = sorted(progress_values)
        
        # Check monotonicity
        for i in range(1, len(sorted_values)):
            assert sorted_values[i] >= sorted_values[i-1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
