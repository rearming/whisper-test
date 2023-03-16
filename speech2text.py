import argparse
import datetime
import math
import os
import textwrap
import openai
from pydub import AudioSegment

OPENAI_API_KEY = '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'


def split_audio_file(file_path, chunk_size_minutes):
    # Determine expected chunk filenames
    basename, ext = os.path.splitext(os.path.basename(file_path))
    dir_name = os.path.join(os.getcwd(), 'splitted_audio', basename)
    os.makedirs(dir_name, exist_ok=True)
    chunk_filenames = [os.path.join(dir_name, f"{basename}-p{i + 1}.mp3")
                       for i in range(math.ceil(AudioSegment.from_file(file_path).duration_seconds / (chunk_size_minutes * 60)))]

    # Check for existing chunk files
    existing_files = [f for f in chunk_filenames if os.path.exists(f)]
    if existing_files:
        print(f"Skipping {len(existing_files)} existing chunks...")
        chunk_filenames = [f for f in chunk_filenames if f not in existing_files]

    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Calculate chunk size in milliseconds
    chunk_size_ms = chunk_size_minutes * 60 * 1000

    # Split the audio into chunks
    audio_chunks = [audio[i:i + chunk_size_ms] for i in range(0, len(audio), chunk_size_ms)]

    # Save the chunks as MP3 files and store their filenames
    filenames = existing_files
    for idx, chunk in enumerate(audio_chunks):
        filename = chunk_filenames[idx]
        chunk.export(filename, format="mp3")
        filenames.append(filename)

    return filenames


def prepare(input_file_path, split):
    if split == -1:
        return [input_file_path]
    return split_audio_file(input_file_path, int(split))


def get_path_name(audio_file_pathname):
    now = datetime.datetime.now()
    path = os.path.join(os.getcwd(), args.out)
    os.makedirs(path, exist_ok=True)
    audio_name = os.path.basename(audio_file_pathname)
    filename = audio_name + '_{}.txt'.format(now.strftime('%Y-%m-%d_%H-%M-%S'))
    return os.path.join(path, filename)


def main():
    openai.api_key = OPENAI_API_KEY

    audio_file_pathname = args.audio
    split = args.split

    pathname = get_path_name(audio_file_pathname)
    audio_chunks = prepare(audio_file_pathname, split)

    transcripts = []

    for chunk in audio_chunks:
        chunk_file = open(chunk, "rb")
        transcript = openai.Audio.transcribe('whisper-1', chunk_file, prompt=args.prompt, language=args.lang)
        transcripts.append(transcript)

    with open(pathname, 'w') as chunk_file:
        for i, transcript in enumerate(transcripts):
            filename = os.path.basename(transcript.get('file_name', ''))
            text = transcript.get('text', '')
            output = f"<-- {filename} file {i + 1} -->\n\n{text}\n\n"
            output = '\n'.join(textwrap.wrap(output, width=120)) + '\n'
            chunk_file.write(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='test-whisper')
    parser.add_argument('audio', type=str, default='', help='Input audio file path')
    parser.add_argument('--split', type=int, default=-1,
                        help='If specified, means audio will be split into chunks of this size (in minutes)')
    parser.add_argument('--prompt', type=str, default='', help='Prompt to help the model recognise audio.')
    parser.add_argument('--lang', type=str, default='en', help='Language of audio')
    parser.add_argument('--out', type=str, default='transcripts', help='Output directory for speech2text results')
    args = parser.parse_args()
    main()
