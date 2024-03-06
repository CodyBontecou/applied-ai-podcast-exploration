"""
Attempting to pull all of the pieces together.
"""

from transcribe import transcribe_audio_file
from chat import chat_with_chatGPT
from extract_audio import extract_audio_segment
from local_whisper import generate_json_segments
from split_text_to_lines import process_video

audio_file = 'split_12.wav'
result = transcribe_audio_file(audio_file)
gpt_json = chat_with_chatGPT(result)

for i in range(3):
  segment = data['segments'][i]
  extract_audio_segment(audio_file, segment['start'], segment['end'], f'split_17_output-{i}.wav')
  generate_json_segments(f'split_17_output-{i}.wav')


with open(f'local_whisper-{2}.json', 'r') as f:
    wordlevel_info_modified = json.load(f)

process_video(wordlevel_info_modified, 2)
