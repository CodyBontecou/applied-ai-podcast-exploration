"""
This uses the local whisper model to transcribe the split 
.wav files into their own individual JSON segments
with the data structure:

  [
    {
        "word": "I",
        "start": 0.0,
        "end": 0.14
    },
    ...,
  ]
"""

import json
import whisper

def generate_json_segments(audio_file, i):
  model = whisper.load_model("medium")
  result = model.transcribe(audio_file, word_timestamps=True)

  wordlevel_info = []

  for each in result['segments']:
    words = each['words']
    for word in words:
      wordlevel_info.append({'word':word['word'].strip(),'start':word['start'],'end':word['end']})


  # replaces the audio file's .wav extension with .json
  with open(f'{i}-{audio_file.replace(".wav", ".json")}', 'w') as f:
      json.dump(wordlevel_info, f, indent=4)

  return wordlevel_info
