
import json
from pydub import AudioSegment

def extract_audio_segment(file_path, start_time, end_time, output_file):
    """
    Extracts a segment from an audio file and saves it to a new file.

    Parameters:
    - file_path: Path to the original audio file.
    - start_time: Start time of the segment to extract, in seconds.
    - end_time: End time of the segment to extract, in seconds.
    - output_file: Path to save the extracted audio segment.
    """
    # Convert start and end times from seconds to milliseconds
    start_time_ms = int(start_time * 1000)
    end_time_ms = int(end_time * 1000)

    print(start_time, start_time_ms)

    # Load the audio file
    audio = AudioSegment.from_file(f'{file_path}.wav')

    # Extract the specified segment
    extracted_segment = audio[start_time_ms:end_time_ms]

    # Save the extracted segment to a new file
    extracted_segment.export(output_file, format="wav")
