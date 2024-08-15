import speech_recognition as sr
from circles_of_trust import CirclesOfTrust
import pveagle
from pvrecorder import PvRecorder
import os
import bulb_devices_functions
import plug_devices_functions

#SPEAKER RECOGNIZER KEY
access_key = "SuA+bf3Nm1N5wbr9J7qSXFNvX7aiLDn2xShnDXg0opLPYPLx2gGjNA=="


# Initialize recognizer
recognizer = sr.Recognizer()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to transcribe speech
def transcribe_audio(access_control):
    # Open profiles
    # Load the saved speaker profiles from bytes
    with open("../voice-recognition/speaker-recognition/speaker_profile_1.dat", "rb") as f:
        speaker_profile_1_bytes = f.read()
        print(f'opened speaker 1 profile')

    with open("../voice-recognition/speaker-recognition/speaker_profile_2.dat", "rb") as f:
        speaker_profile_2_bytes = f.read()
        print(f'opened speaker 2 profile')

    speaker_profile_1 = pveagle.EagleProfile.from_bytes(speaker_profile_1_bytes)
    speaker_profile_2 = pveagle.EagleProfile.from_bytes(speaker_profile_2_bytes)

    profiles = [speaker_profile_1, speaker_profile_2]

    print(profiles)
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

    ############# TRANSCRIBE ###################

    with sr.Microphone() as source:
        clear_console()
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio_frame = recorder.read()
                score = eagle.process(audio_frame)
                # Listen for audio input with a timeout
                audio = recognizer.listen(source, timeout=5)
                
                #testing
                print(audio_frame)
                # Process audio in chunks for real-time transcription
                chunks = recognizer.recognize_google(audio, show_all=True)

                # Iterate over the recognized chunks and print words incrementally
                for chunk in chunks['alternative']:
                    if 'transcript' in chunk:
                        if (len(score) > 0):
                            print("You said:", chunk['transcript'])
                            process_command(speaker_profile_1, chunk['transcript'], access_control)
            
            except sr.WaitTimeoutError:
                print("Continue listening...")
            except sr.UnknownValueError:
                pass  # Ignore if the speech is not understood
            except sr.RequestError as e:
                print("Error fetching results from Google Speech Recognition; {0}".format(e))
            finally:
                recorder.stop()
                recorder.delete()
                eagle.delete()


def process_command(user, sentence, access_control):
    command_map = {
        'red': 'set_red',
        'blue': 'set_blue',
        'green': 'set_green',
        'yellow': 'set_yellow',
        'purple': 'set_purple',
        'orange': 'set_orange',
        'pink': 'set_pink',
        'indigo': 'set_indigo',
        'cyan': 'set_cyan',
        'magenta': 'set_magenta',
        'teal': 'set_teal',
        'lime': 'set_lime',
        'white': 'set_white_color',
        'brighten': 'increase_brightness',
        'dim': 'decrease_brightness',
        'off': 'plug_off',
        'on': 'plug_on'
    }

    # Tokenize the sentence
    words = sentence.lower().split()

    functionality_name = None
    for word in words:
        if word in command_map:
            functionality_name = command_map[word]
            # Determine the device type based on the functionality name
            if functionality_name in ['set_red', 'set_blue', 'set_green', 'set_yellow', 'set_purple',
                                      'set_orange', 'set_pink', 'set_indigo', 'set_cyan', 'set_magenta',
                                      'set_teal', 'set_lime', 'set_white_color', 'increase_brightness',
                                      'decrease_brightness']:
                device_type = 'light'
            elif functionality_name in ['plug_off', 'plug_on']:
                device_type = 'plug'
            else:
                device_type = 'unknown'

            try:
                # Execute the device functionality
                access_control.execute_device_functionality(user, functionality_name, device_type)
                print(f"Executed {functionality_name} for {user}.")
            except ValueError as e:
                print(f"Failed to execute functionality: {e}")
            break  # Stop processing after the first valid command
    else:
        print(f"No valid command found in: {sentence}")