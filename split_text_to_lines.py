"""
This takes the json file generated in local_whisper.py
and builds a video with highlighted text
"""

import json

from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, ColorClip, ImageClip

import numpy as np


def process_video(wordlevel_info_modified, file_number, audio_file):
    def split_text_into_lines(data):  

      MaxChars = 80 
      #maxduration in seconds
      MaxDuration = 3.0
      #Split if nothing is spoken (gap) for these many seconds
      MaxGap = 1.5

      subtitles = []
      line = []
      line_duration = 0
      line_chars = 0


      for idx,word_data in enumerate(data):
          word = word_data["word"]
          start = word_data["start"]
          end = word_data["end"]

          line.append(word_data)
          line_duration += end - start
          
          temp = " ".join(item["word"] for item in line)
          

          # Check if adding a new word exceeds the maximum character count or duration
          new_line_chars = len(temp)

          duration_exceeded = line_duration > MaxDuration 
          chars_exceeded = new_line_chars > MaxChars 
          if idx>0:
            gap = word_data['start'] - data[idx-1]['end'] 
            # print (word,start,end,gap)
            maxgap_exceeded = gap > MaxGap
          else:
            maxgap_exceeded = False
          

          if duration_exceeded or chars_exceeded or maxgap_exceeded:
              if line:
                  subtitle_line = {
                      "word": " ".join(item["word"] for item in line),
                      "start": line[0]["start"],
                      "end": line[-1]["end"],
                      "textcontents": line
                  }
                  subtitles.append(subtitle_line)
                  line = []
                  line_duration = 0
                  line_chars = 0


      if line:
          subtitle_line = {
              "word": " ".join(item["word"] for item in line),
              "start": line[0]["start"],
              "end": line[-1]["end"],
              "textcontents": line
          }
          subtitles.append(subtitle_line)

      return subtitles

    def create_caption(textJSON, framesize, font="Helvetica-Bold", fontsize=120, color='white', bgcolor='blue', logo_size=(100, 100)):
        wordcount = len(textJSON['textcontents'])
        full_duration = textJSON['end'] - textJSON['start']

        word_clips = []
        xy_textclips_positions =[]
        
        x_pos = 0
        y_pos = 0
        # max_height = 0
        frame_width = framesize[0]
        frame_height = framesize[1]
        x_buffer = frame_width*1/10
        y_buffer = frame_height*1/5

        space_width = ""
        space_height = ""

        for index, wordJSON in enumerate(textJSON['textcontents']):
          duration = wordJSON['end'] - wordJSON['start']
          word_clip = TextClip(wordJSON['word'], font = font,fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
          word_clip_space = TextClip(" ", font=font, fontsize=fontsize, color=color).set_start(textJSON['start']).set_duration(full_duration)
          word_width, word_height = word_clip.size
          space_width,space_height = word_clip_space.size
          if x_pos + word_width + space_width > frame_width-2 * x_buffer:
                # Move to the next line
                x_pos = 0
                y_pos = y_pos+ word_height+40

                # Store info of each word_clip created
                xy_textclips_positions.append({
                    "x_pos":x_pos+x_buffer,
                    "y_pos": y_pos+y_buffer,
                    "width" : word_width,
                    "height" : word_height,
                    "word": wordJSON['word'],
                    "start": wordJSON['start'],
                    "end": wordJSON['end'],
                    "duration": duration
                })

                word_clip = word_clip.set_position((x_pos+x_buffer, y_pos+y_buffer))
                word_clip_space = word_clip_space.set_position((x_pos+ word_width +x_buffer, y_pos+y_buffer))
                x_pos = word_width + space_width
          else:
                # Store info of each word_clip created
                xy_textclips_positions.append({
                    "x_pos":x_pos+x_buffer,
                    "y_pos": y_pos+y_buffer,
                    "width" : word_width,
                    "height" : word_height,
                    "word": wordJSON['word'],
                    "start": wordJSON['start'],
                    "end": wordJSON['end'],
                    "duration": duration
                })

                word_clip = word_clip.set_position((x_pos+x_buffer, y_pos+y_buffer))
                word_clip_space = word_clip_space.set_position((x_pos+ word_width+ x_buffer, y_pos+y_buffer))

                x_pos = x_pos + word_width+ space_width


          word_clips.append(word_clip)
          word_clips.append(word_clip_space)


        for highlight_word in xy_textclips_positions:
          word_clip_highlight = TextClip(
            highlight_word['word'], 
            font=font,
            fontsize=fontsize,
            color=color,
            bg_color=bgcolor,
            align='center'
          ).set_start(highlight_word['start']).set_duration(highlight_word['duration'])
          word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
          word_clips.append(word_clip_highlight)

        return word_clips
        
    linelevel_subtitles = split_text_into_lines(wordlevel_info_modified)
    frame_size = (1080, 1920)
    all_line_level_splits = []
    for line in linelevel_subtitles:
        out = create_caption(line, frame_size)
        all_line_level_splits.extend(out)

    input_audio = AudioFileClip(f'{audio_file}_output-{file_number}.wav')
    input_audio_duration = input_audio.duration
    
    background_clip = ColorClip(size=frame_size, color=(0, 0, 0)).set_duration(input_audio_duration)
    logo_path = 'logo.png' # Path to your logo image
    logo_clip = ImageClip(logo_path).set_duration(input_audio_duration)
    
    logo_x = frame_size[0] - logo_clip.size[0] - 10 # Adjust the X position as needed
    logo_y = frame_size[1] - logo_clip.size[1] - 10 # Adjust the Y position as needed
    
    logo_clip = logo_clip.set_position((logo_x, logo_y))
    
    background_with_logo = CompositeVideoClip([background_clip])
    
    final_video = CompositeVideoClip([background_with_logo] + all_line_level_splits)
    
    final_video = final_video.set_audio(input_audio)
    
    final_video.write_videofile(f"output-{file_number}.mp4", fps=24, codec="libx264", audio_codec="aac")
