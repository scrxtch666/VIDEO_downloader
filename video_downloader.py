import yt_dlp
import argparse
import os
import sys

def download_video(url, output_dir='.', format_quality='best'):
    """
    Download video from given URL in single format (no merging required).
    
    Args:
        url (str): URL of the video to download
        output_dir (str): Directory to save the downloaded video
        format_quality (str): Quality setting (default to best single format)
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.expanduser(output_dir)  # Expand ~ to user directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Configuration options
    ydl_opts = {
        'format': format_quality,  # Using 'best' to get the best single format
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': False,
        'verbose': False,  # Less verbose output
    }
    
    print(f"Downloading video from: {url}")
    print(f"Saving to directory: {output_dir}")
    print(f"Quality setting: {format_quality}")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                print(f"Video found: {info.get('title', 'Unknown Title')}")
                print(f"Duration: {info.get('duration', 'Unknown')} seconds")
                
                # Download the video
                ydl.download([url])
                
                # Verify download was successful
                downloaded_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
                if downloaded_files:
                    print("\nDownload completed successfully!")
                    print(f"Files in {output_dir}:")
                    for file in downloaded_files:
                        file_path = os.path.join(output_dir, file)
                        size_mb = os.path.getsize(file_path) / (1024 * 1024)
                        print(f" - {file} ({size_mb:.2f} MB)")
                else:
                    print("\nWarning: No files found in output directory after download.")
            else:
                print("Error: Could not extract video information.")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='Download videos in highest quality')
    parser.add_argument('url', help='URL of the video to download')
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    parser.add_argument('--quality', '-q', default='best', 
                        help='Video quality (default: best)')
    
    args = parser.parse_args()
    sys.exit(download_video(args.url, args.output, args.quality))

if __name__ == "__main__":
    main()