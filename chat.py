"""
Passes the text from transcribe.py with a prompt to ChatGPT.
This extracts three key points from the provided text and returns it in
JSON format.
"""

from openai import OpenAI
from dotenv import load_dotenv


def chat_with_chatGPT(transcript_text):
  load_dotenv()
  client = OpenAI()

  generate_prompt = lambda text : f"""
    ${text} Give me three sections of text extracted from this block of text that you believe to be the most interesting and worth sharing with others. Make sure the sections of text are at least 50 words longs. Give me three segments that you believe to be interesting and worth sharing. Do not return any text that isn't a part of the above segments. Give me the time stamps of the beginning and ends of each segment. Return the data structured like: 

    start: start time,
    end: end time,
    text: text

  """

  # with open('split_17.txt', 'r') as file:
  #     transcript_text = file.read()

  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
      {"role": "user", "content": generate_prompt(transcript_text)}
    ]
  )

  gpt_json = response.choices[0].message.content


  with open('chat_response.json', 'w') as f:
      f.write(gpt_json)

  return gpt_json