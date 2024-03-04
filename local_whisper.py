import json
import whisper

model = whisper.load_model("medium")
result = model.transcribe('split_17_output-0.wav', word_timestamps=True)

wordlevel_info = []

for each in result['segments']:
  words = each['words']
  for word in words:
    wordlevel_info.append({'word':word['word'].strip(),'start':word['start'],'end':word['end']})


with open('local_whisper-0.json', 'w') as f:
    json.dump(wordlevel_info, f,indent=4)
