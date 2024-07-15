import pveagle
from pvrecorder import PvRecorder
import time

# ENROLLMENT
access_key = "c+eQ86/5gX5Z6rypq5n2Wq9q+wxp+e+FUkEvFpsWXGQp+cNLJAg8pg=="
try:
    eagle_profiler = pveagle.create_profiler(access_key=access_key)
except pveagle.EagleError as e:
    # Handle error
    print(f"Error creating profiler: {e}")
    exit(1)

DEFAULT_DEVICE_INDEX = -1
recorder = PvRecorder(
    device_index=DEFAULT_DEVICE_INDEX,
    frame_length=eagle_profiler.min_enroll_samples)

try:
    recorder.start()
except Exception as e:
    # Handle error
    print(f"Error starting recorder: {e}")
    eagle_profiler.delete()
    exit(1)

# Function to enroll a speaker
def enroll_speaker():
    enroll_percentage = 0.0
    while enroll_percentage < 100.0:
        audio_frame = recorder.read()
        enroll_percentage, feedback = eagle_profiler.enroll(audio_frame)
        print(f"Enrollment progress: {enroll_percentage}% - Feedback: {feedback}")

# Enroll the first speaker
print("Enrolling first speaker...")
enroll_speaker()
print("First speaker enrolled.")

# Save the first speaker profile
speaker_profile_1 = eagle_profiler.export()

# Wait for 5 seconds before enrolling the second speaker
print("Waiting for 5 seconds before enrolling the second speaker...")
time.sleep(5)

# Reset profiler to enroll the second speaker
try:
    eagle_profiler.reset()
except pveagle.EagleError as e:
    # Handle error
    print(f"Error resetting profiler: {e}")
    recorder.stop()
    recorder.delete()
    eagle_profiler.delete()
    exit(1)

# Enroll the second speaker
print("Enrolling second speaker...")
enroll_speaker()
print("Second speaker enrolled.")

# Save the second speaker profile
speaker_profile_2 = eagle_profiler.export()

recorder.stop()
recorder.delete()
eagle_profiler.delete()

# Save both speaker profiles as bytes for later use
with open("speaker_profile_1.dat", "wb") as f:
    f.write(speaker_profile_1.to_bytes())

with open("speaker_profile_2.dat", "wb") as f:
    f.write(speaker_profile_2.to_bytes())

print("Both speaker profiles have been saved.")
