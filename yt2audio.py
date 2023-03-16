import argparse
import logging
import os
import pytube

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def download_audio(url, directory):
    try:
        youtube_video = pytube.YouTube(url)
        logging.info("Video information fetched.")
        audio_stream = youtube_video.streams.filter(only_audio=True).first()
        if not os.path.exists(directory):
            os.makedirs(directory)
        logging.info(f"Downloading audio from {url}")
        file_path = audio_stream.download(output_path=directory, filename_prefix="audio")
        logging.info(f"Download completed. File saved to {file_path}")
        os.rename(file_path, os.path.join(directory, f"{args.name if args.name else youtube_video.title}.mp3"))
        logging.info("Conversion to mp3 format completed.")
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='youtube2audio')
    parser.add_argument('url', type=str, default='', help='URL of youtube video')
    parser.add_argument('--out', type=str, default='', help='Output directory')
    parser.add_argument('--name', type=str, default='', help='Name of file created')
    args = parser.parse_args()
    download_audio(args.url, args.out)
