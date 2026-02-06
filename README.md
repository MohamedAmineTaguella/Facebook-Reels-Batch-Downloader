# Facebook Reels Batch Downloader

<img src="https://via.placeholder.com/800x450/2b2d42/ffffff?text=Facebook+Reels+Downloader+GUI" alt="Screenshot" width="700"/>

**Simple desktop GUI application** that lets you batch-download **Facebook Reels** (and regular FB videos) using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Just put all your reel/video links into a file called `links.txt` (one link per line) and press the big START button.

## Features

- Modern looking interface (customtkinter)
- Batch downloading from `links.txt`
- Choose custom output folder (or use current directory)
- Live download progress & logs in the app
- Dark / Light / System appearance mode
- Retries automatically on network issues
- Merges best video + audio → MP4

## Requirements

- Windows / macOS / Linux
- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (will be checked automatically)

## Installation

### Option 1: Run from source (recommended for testing)

1. Clone the repo

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
