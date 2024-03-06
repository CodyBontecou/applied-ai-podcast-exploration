"""
Uses whisper-large-v3 model from an online repository
to convert the provided audio file into a txt file.

The txt file contains the text and time chunks.
"""

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def transcribe_audio_file(file_name):
  device = "cuda:0" if torch.cuda.is_available() else "cpu"
  torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

  model_id = "openai/whisper-large-v3"

  model = AutoModelForSpeechSeq2Seq.from_pretrained(
      model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
  )
  model.to(device)

  processor = AutoProcessor.from_pretrained(model_id)

  # TODO: Timestamps appear to be slightly off.
  pipe = pipeline(
      "automatic-speech-recognition",
      model=model,
      tokenizer=processor.tokenizer,
      feature_extractor=processor.feature_extractor,
      max_new_tokens=128,
      chunk_length_s=20,
      batch_size=8,
      return_timestamps=True,
      torch_dtype=torch_dtype,
      device=device
  )


  result = pipe(f'{file_name}.wav')

  with open(f'{file_name}.txt', 'w') as f:
      f.write(result)
  
  return result
