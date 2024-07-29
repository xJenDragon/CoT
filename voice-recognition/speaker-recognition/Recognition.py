import pveagle
from pvrecorder import PvRecorder
import time
import os

# RECOGNITION
access_key = "7fI/+XvnUCxALsxBP7kIG/p5eAu9Ksk7mhIgw/X0CWd+fltMbHZYOw=="

# Load the saved speaker profiles from bytes
with open("speaker_profile_1.dat", "rb") as f:
    speaker_profile_1_bytes = f.read()

with open("speaker_profile_2.dat", "rb") as f:
    speaker_profile_2_bytes = f.read()

speaker_profile_1 = pveagle.EagleProfile.from_bytes(speaker_profile_1_bytes)
speaker_profile_2 = pveagle.EagleProfile.from_bytes(speaker_profile_2_bytes)

print("Speaker Profile 1 Loaded:", speaker_profile_1)
print("Speaker Profile 2 Loaded:", speaker_profile_2)

profiles = [speaker_profile_1, speaker_profile_2]
try:
    eagle = pveagle.create_recognizer(
        access_key=access_key,
        speaker_profiles=profiles)
except pveagle.EagleError as e:
    # Handle error
    print(f"Error creating recognizer: {e}")
    exit(1)

DEFAULT_DEVICE_INDEX = -1
recorder = PvRecorder(
    device_index=DEFAULT_DEVICE_INDEX,
    frame_length=eagle.frame_length)

try:
    recorder.start()
except Exception as e:
    # Handle error
    print(f"Error starting recorder: {e}")
    eagle.delete()
    exit(1)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_bars(scores, max_length=50):
    clear_console()
    print("Recognition Scores")
    print("==================")
    for i, score in enumerate(scores):
        bar_length = int(score * max_length)
        bar = '=' * bar_length
        print(f"Speaker {i + 1}: [{bar:<{max_length}}] {score:.2f}")

print("Recognition started. Press Ctrl+C to stop.")
try:
    while True:
        audio_frame = recorder.read()
        scores = eagle.process(audio_frame)
        print("Scores:", scores)  # Debugging line to check scores
        display_bars(scores)
        time.sleep(0.1)  # Adjust the sleep time as necessary
except KeyboardInterrupt:
    print("Recognition stopped by user.")
finally:
    recorder.stop()
    recorder.delete()
    eagle.delete()
