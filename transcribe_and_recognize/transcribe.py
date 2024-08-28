from pvrecorder import PvRecorder
import pveagle
import os

access_key = "SuA+bf3Nm1N5wbr9J7qSXFNvX7aiLDn2xShnDXg0opLPYPLx2gGjNA=="
eagle_profiler = pveagle.create_profiler(access_key)

def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')

recorder = PvRecorder(
  frame_length=eagle_profiler.min_enroll_samples,
  device_index=0)

try:
  recorder.start()
except:
  print("Error starting recorder")
finally:
  print('Recording')




def get_next_enroll_audio_data(): 

  """Enrolling the user"""


  percentage = 0.0
  while percentage < 100.0:
      
      
      """Collecting the audio frame to hear the users voice."""


      audio_frame = recorder.read()


      """Enrolling the user using the audio_frame data that's being collected."""


      percentage, feedback = eagle_profiler.enroll(audio_frame)


      """Printing the percentage in how much of the users voice has been fully enrolled."""

      clear_console()
      print(f"{feedback.name}, {percentage}")


speaker_profiles = []
num_speaker_profiles = 2
for i in range (num_speaker_profiles):
  print(f'Enrolling Speaker {i+1}...')
  get_next_enroll_audio_data()
  print(f'Speaker {i+1} Enrolled')
  speaker_profiles.append(eagle_profiler.export())
  eagle_profiler.reset()

recorder.stop()

"""RECOGNITION"""

recorder = PvRecorder(
  frame_length=512,
  device_index=0)

eagle = pveagle.create_recognizer(access_key, speaker_profiles)


try:
  while True:
    recorder.start()
    recognition_audio_frame = recorder.read()
    score = eagle.process(recognition_audio_frame)
    clear_console()
    for i, profile in enumerate(speaker_profiles):
      print(f"Speaker {i+1}: {score[i]}")

except Exception as e:
  print(f"Error processing audio for recognition. Error: {e}")

finally:
  eagle_profiler.delete()
  recorder.delete()
  eagle.delete()




