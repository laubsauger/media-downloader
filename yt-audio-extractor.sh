#!/bin/bash

# This script downloads the audio from a YouTube video and saves it as a WAV file.
# It requires one argument: the YouTube video URL.
# It depends on ffmpeg for audio conversion and will download yt-dlp locally if not present.

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if a URL is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <youtube_url>"
  exit 1
fi

# Check for ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg could not be found. Please install it first."
    exit 1
fi

# Check for yt-dlp, download if not present
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp not found, downloading..."
    curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o yt-dlp
    chmod +x yt-dlp
    YT_DLP="./yt-dlp"
else
    YT_DLP="yt-dlp"
fi

# Download and convert audio
echo "Downloading and converting audio..."
$YT_DLP -x --audio-format wav -o "%(title)s.%(ext)s" "$1"

echo "Done."
