import yt_dlp
import argparse
import os
import sys
from colorama import Fore, Style, init
from tabulate import tabulate
from rich.text import Text
from rich.console import Console

# VIDEO DOWNLOADER V2 by @scrxtch & Claude.ai

init(autoreset=True)
console = Console()

def format_duration(seconds):
   
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes} min {seconds} sec"

def download_video(url, output_dir='.', format_quality='best'):
 
   
    output_dir = os.path.expanduser(output_dir) 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

   
    ydl_opts = {
        'format': format_quality,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': False,
        'verbose': False,
    }

    
    console.print("=" * 60, style="cyan")
    console.print("📥  [bold cyan]Downloading video from:[/bold cyan]")
    console.print(f"🎬  URL: [yellow]{url}[/yellow]")
    console.print(f"📁  Directory: [yellow]{output_dir}[/yellow]")
    console.print("-" * 60, style="magenta")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                video_title = info.get('title', 'Unknown Title')
                video_duration = format_duration(info.get('duration', 0))

                
                console.print(f"🎥  Video found: [bold white]{video_title}[/bold white]")
                console.print(f"⏳  Duration: [green]{video_duration}[/green]")

                console.print("=" * 60, style="cyan")

               
                ydl.download([url])

               
                downloaded_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
                if downloaded_files:
                    console.print("\n✅  [bold green]Download completed successfully![/bold green]")
                    console.print(f"📂 Files in [yellow]{output_dir}[/yellow]:\n")

                    table_data = []
                    for file in downloaded_files:
                        file_path = os.path.join(output_dir, file)
                        size_mb = os.path.getsize(file_path) / (1024 * 1024)
                        table_data.append([file, f"{size_mb:.2f} MB"])

                    
                    console.print(tabulate(table_data, headers=["File Name", "Size"], tablefmt="grid"))
                else:
                    console.print("\n⚠️  [bold yellow]Warning: No files found in the output directory after download.[/bold yellow]")
            else:
                console.print("❌  [bold red]Error: Could not extract video information.[/bold red]")
    except Exception as e:
        console.print(f"❌  [bold red]Error downloading video: {e}[/bold red]")
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
