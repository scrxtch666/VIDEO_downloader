# Video Downloader

A simple command-line tool to download videos from various websites using yt-dlp.

## Description

Video Downloader is a Python script that provides a user-friendly interface for the popular yt-dlp library. It allows you to easily download videos from a wide range of websites in your preferred quality and save them to a specified directory.

## Features

- Download videos from numerous websites
- Specify output directory
- Select video quality
- Automatic creation of output directory if it doesn't exist
- Detailed download information and progress
- File size reporting upon completion

## Prerequisites

- Python 3.6 or higher
- yt-dlp library
- websockets library (for browser impersonation)

## Installation

1. Clone this repository:
   ```
   https://github.com/scrxtch666/VideoDownloader.git
   ```

2. Install the required dependencies:
   ```
   pip install yt-dlp websockets
   ```

## Usage

Basic usage:
```
python video_downloader.py URL [--output OUTPUT_DIR] [--quality QUALITY]
```

### Parameters

- `URL` - The URL of the video you want to download (required)
- `--output`, `-o` - Directory where the video will be saved (default: current directory)
- `--quality`, `-q` - Video quality setting (default: 'best')

### Examples

Download a video in the best available quality to the current directory:
```
python video_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Download to a specific directory:
```
python video_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --output ~/Downloads/Videos
```

Download a specific quality:
```
python video_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --quality "best[height<=720]"
```

## Troubleshooting

### HTTP Error 403: Forbidden

If you encounter a "403 Forbidden" error, it may be because the website is blocking automated downloads. Install the websockets library to enable browser impersonation:

```
pip install websockets
```

### Other Issues

- Make sure you have the latest version of yt-dlp:
  ```
  pip install --upgrade yt-dlp
  ```

- For sites with strict access controls, try using browser cookies:
  ```
  python video_downloader.py URL --output OUTPUT_DIR --cookies-from-browser chrome
  ```
  (Note: This requires modifying the script to support the additional parameters)

## Legal Notice

This tool should only be used to download content for which you have permission or that is freely available for download. The user is responsible for complying with all applicable laws and terms of service for the websites from which they download content.

## License

This project is licensed under the MIT License - see the LICENSE file for details.