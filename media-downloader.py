#!/usr/bin/env python3
"""
Flexible media downloader supporting multiple platforms.
Currently supports: YouTube, Instagram
"""

import argparse
import subprocess
import sys
import os
import re
import json
from urllib.parse import urlparse
from pathlib import Path


class MediaDownloader:
    """Base class for media downloaders"""
    
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.yt_dlp_path = self._ensure_yt_dlp()
    
    def _ensure_yt_dlp(self):
        """Ensure yt-dlp is available"""
        # Check if yt-dlp is in PATH
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
            return "yt-dlp"
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check for local yt-dlp
        local_yt_dlp = Path("./yt-dlp")
        if local_yt_dlp.exists():
            return "./yt-dlp"
        
        # Download yt-dlp
        print("yt-dlp not found, downloading...")
        try:
            subprocess.run([
                "curl", "-L", 
                "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp",
                "-o", "yt-dlp"
            ], check=True)
            subprocess.run(["chmod", "+x", "yt-dlp"], check=True)
            return "./yt-dlp"
        except subprocess.CalledProcessError as e:
            print(f"Failed to download yt-dlp: {e}")
            sys.exit(1)
    
    def download(self, url, audio_only=True, format="wav", keep_video=False):
        """Download media from URL"""
        raise NotImplementedError("Subclasses must implement download()")


class YouTubeDownloader(MediaDownloader):
    """YouTube specific downloader"""
    
    def is_youtube_url(self, url):
        """Check if URL is a YouTube URL"""
        patterns = [
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be)',
            r'(https?://)?(www\.)?youtube\.com/watch\?v=',
            r'(https?://)?(www\.)?youtu\.be/'
        ]
        return any(re.match(pattern, url) for pattern in patterns)
    
    def download(self, url, audio_only=True, format="wav", keep_video=False, extra_args=None):
        """Download YouTube media"""
        if not self.is_youtube_url(url):
            raise ValueError("Not a valid YouTube URL")
        
        output_template = str(self.output_dir / "%(title)s.%(ext)s")
        
        cmd = [self.yt_dlp_path]
        
        # Add extra arguments first if provided
        if extra_args:
            cmd.extend(extra_args)
        
        # Only add format options if not listing formats
        if not extra_args or "--list-formats" not in extra_args:
            if audio_only:
                cmd.extend(["-x", "--audio-format", format])
                if keep_video:
                    cmd.append("-k")
            else:
                # Download best quality video+audio, merge if needed
                cmd.extend(["-f", "bestvideo+bestaudio/best"])
        
        cmd.extend(["-o", output_template, url])
        
        print(f"Downloading from YouTube: {url}")
        try:
            subprocess.run(cmd, check=True)
            print("Download completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e}")
            sys.exit(1)


class InstagramDownloader(MediaDownloader):
    """Instagram specific downloader"""
    
    def is_instagram_url(self, url):
        """Check if URL is an Instagram URL"""
        patterns = [
            r'(https?://)?(www\.)?instagram\.com/p/',
            r'(https?://)?(www\.)?instagram\.com/reel/',
            r'(https?://)?(www\.)?instagram\.com/tv/',
            r'(https?://)?(www\.)?instagram\.com/stories/'
        ]
        return any(re.match(pattern, url) for pattern in patterns)
    
    def download(self, url, audio_only=True, format="wav", keep_video=False, extra_args=None):
        """Download Instagram media"""
        if not self.is_instagram_url(url):
            raise ValueError("Not a valid Instagram URL")
        
        output_template = str(self.output_dir / "%(title)s.%(ext)s")
        
        cmd = [self.yt_dlp_path]
        
        # Add extra arguments first if provided
        if extra_args:
            cmd.extend(extra_args)
        
        # Instagram-specific options
        # For stories, download all items in the story
        if '/stories/' not in url:
            cmd.extend(["--no-playlist"])
        
        # Only add format options if not listing formats
        if not extra_args or "--list-formats" not in extra_args:
            if audio_only:
                cmd.extend(["-x", "--audio-format", format])
                if keep_video:
                    cmd.append("-k")
            else:
                # Download best quality video+audio, merge if needed
                cmd.extend(["-f", "bestvideo+bestaudio/best"])
        
        cmd.extend(["-o", output_template, url])
        
        print(f"Downloading from Instagram: {url}")
        try:
            subprocess.run(cmd, check=True)
            print("Download completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e}")
            print("\nNote: Instagram downloads may require authentication.")
            print("You can provide cookies using one of these options:")
            print("  --cookies-from-browser chrome  (or firefox, safari, etc.)")
            print("  --cookies /path/to/cookies.txt")
            sys.exit(1)


class UniversalDownloader:
    """Main downloader that delegates to platform-specific downloaders"""
    
    def __init__(self, output_dir="downloads"):
        self.downloaders = {
            'youtube': YouTubeDownloader(output_dir),
            'instagram': InstagramDownloader(output_dir)
        }
    
    def detect_platform(self, url):
        """Detect which platform the URL belongs to"""
        for name, downloader in self.downloaders.items():
            if name == 'youtube' and downloader.is_youtube_url(url):
                return 'youtube'
            elif name == 'instagram' and downloader.is_instagram_url(url):
                return 'instagram'
        
        # Try generic yt-dlp as fallback
        return 'generic'
    
    def download(self, url, audio_only=True, format="wav", platform=None, keep_video=False, extra_args=None):
        """Download media from any supported platform"""
        if platform is None:
            platform = self.detect_platform(url)
        
        if platform == 'generic':
            print(f"Platform not specifically supported, trying generic download...")
            # Use YouTube downloader as generic since it uses yt-dlp
            downloader = self.downloaders['youtube']
            # Override the URL check for generic downloads
            output_template = str(Path("downloads") / "%(title)s.%(ext)s")
            
            cmd = [downloader.yt_dlp_path]
            
            # Add extra arguments first if provided
            if extra_args:
                cmd.extend(extra_args)
            
            # Only add format options if not listing formats
            if not extra_args or "--list-formats" not in extra_args:
                if audio_only:
                    cmd.extend(["-x", "--audio-format", format])
                    if keep_video:
                        cmd.append("-k")
                else:
                    # Download best quality video+audio, merge if needed
                    cmd.extend(["-f", "bestvideo+bestaudio/best"])
            
            cmd.extend(["-o", output_template, url])
            
            try:
                subprocess.run(cmd, check=True)
                print("Download completed successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Download failed: {e}")
                sys.exit(1)
        else:
            if platform not in self.downloaders:
                raise ValueError(f"Platform '{platform}' not supported")
            
            downloader = self.downloaders[platform]
            downloader.download(url, audio_only, format, keep_video, extra_args)


def main():
    parser = argparse.ArgumentParser(
        description="Download media from various platforms (YouTube, Instagram, etc.)"
    )
    parser.add_argument("url", help="URL of the media to download")
    parser.add_argument(
        "-v", "--video", 
        action="store_true", 
        help="Download video instead of audio only"
    )
    parser.add_argument(
        "-k", "--keep-video",
        action="store_true",
        help="Keep the video file when extracting audio"
    )
    parser.add_argument(
        "-f", "--format", 
        default="wav", 
        help="Audio format (default: wav). Common: mp3, wav, m4a, flac"
    )
    parser.add_argument(
        "-o", "--output-dir", 
        default="downloads", 
        help="Output directory (default: downloads)"
    )
    parser.add_argument(
        "-p", "--platform", 
        choices=["youtube", "instagram", "generic"],
        help="Force specific platform parser"
    )
    parser.add_argument(
        "--cookies",
        help="Path to cookies file (useful for Instagram)"
    )
    parser.add_argument(
        "--cookies-from-browser",
        help="Browser to extract cookies from (brave, chrome, chromium, edge, firefox, opera, safari, vivaldi, whale)"
    )
    
    # Parse known args and collect remaining as extra args for yt-dlp
    args, extra_args = parser.parse_known_args()
    
    # Add cookies to extra_args if provided
    if args.cookies:
        extra_args.extend(["--cookies", args.cookies])
    
    # Add cookies-from-browser to extra_args if provided
    if args.cookies_from_browser:
        extra_args.extend(["--cookies-from-browser", args.cookies_from_browser])
    
    downloader = UniversalDownloader(args.output_dir)
    
    try:
        downloader.download(
            args.url, 
            audio_only=not args.video,
            format=args.format,
            platform=args.platform,
            keep_video=args.keep_video,
            extra_args=extra_args if extra_args else None
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDownload cancelled by user")
        sys.exit(1)


if __name__ == "__main__":
    main()