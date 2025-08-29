# Media Downloader

A flexible media downloader supporting multiple platforms including YouTube and Instagram.

## Features

- Download audio or video from multiple platforms
- Support for YouTube, Instagram, and other sites via yt-dlp
- Automatic audio extraction and conversion
- Multiple audio format support (wav, mp3, m4a, flac)
- Clean, modular architecture for easy extension

## Installation

The script will automatically download yt-dlp if not present. Make sure you have:
- Python 3.6+
- ffmpeg (for audio conversion)
- curl (for downloading yt-dlp)

## Usage

### Basic usage (download audio as WAV):
```bash
./media-downloader.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Download video instead of audio:
```bash
./media-downloader.py -v https://www.youtube.com/watch?v=VIDEO_ID
```

### Extract audio but keep the video file:
```bash
./media-downloader.py -k https://www.youtube.com/watch?v=VIDEO_ID
```

### Specify audio format:
```bash
./media-downloader.py -f mp3 https://www.youtube.com/watch?v=VIDEO_ID
```

### Download from Instagram:
```bash
./media-downloader.py https://www.instagram.com/p/POST_ID/
```

### Specify output directory:
```bash
./media-downloader.py -o my_downloads https://www.youtube.com/watch?v=VIDEO_ID
```

### Force specific platform parser:
```bash
./media-downloader.py -p instagram https://www.instagram.com/p/POST_ID/
```

## Instagram Downloads

Instagram may require authentication for some content. If you encounter issues:
1. Use a browser extension to export Instagram cookies
2. Save them to a file (e.g., `cookies.txt`)
3. Use with the downloader: `./media-downloader.py --cookies cookies.txt URL`

## Supported Platforms

- **YouTube**: Full support for videos, playlists, and live streams
- **Instagram**: Posts, Reels, and TV videos
- **Generic**: Any site supported by yt-dlp

## Legacy Script

The original `yt-audio-extractor.sh` is still available for simple YouTube audio downloads:
```bash
./yt-audio-extractor.sh https://www.youtube.com/watch?v=VIDEO_ID
```