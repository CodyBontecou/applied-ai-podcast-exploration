"""
Attempting to pull all of the pieces together.
"""

import json
import time

from transcribe import transcribe_audio_file
from chat import chat_with_chatGPT
from extract_audio import extract_audio_segment
from local_whisper import generate_json_segments
from split_text_to_lines import process_video

start_time = time.time()

audio_file = 'split_12'
result = transcribe_audio_file(audio_file)
gpt_json = chat_with_chatGPT(result)
print(gpt_json)

for i in range(3):
  segment = gpt_json['segments'][i]
  extract_audio_segment(audio_file, segment['start'], segment['end'], f'{audio_file}_output-{i}.wav')
  wordlevel_info_modified = generate_json_segments(f'{audio_file}_output-{i}.wav', i)
  process_video(wordlevel_info_modified, i, audio_file)

end_time = time.time()
duration = end_time - start_time
print(f"The function took {duration} seconds to complete.")
