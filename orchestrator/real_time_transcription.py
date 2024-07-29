import speech_recognition as sr
from circles_of_trust import CirclesOfTrust
import bulb_devices_functions
import plug_devices_functions

# Initialize recognizer
recognizer = sr.Recognizer()


# Function to transcribe speech
def transcribe_audio(access_control):
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                # Listen for audio input with a timeout
                audio = recognizer.listen(source, timeout=5)

                # Process audio in chunks for real-time transcription
                chunks = recognizer.recognize_google(audio, show_all=True)

                # Iterate over the recognized chunks and print words incrementally
                for chunk in chunks['alternative']:
                    if 'transcript' in chunk:
                        user = 'untrusted'
                        print("You said:", chunk['transcript'])
                        process_command(user, chunk['transcript'], access_control)
            except sr.WaitTimeoutError:
                print("Continue listening...")
            except sr.UnknownValueError:
                pass  # Ignore if the speech is not understood
            except sr.RequestError as e:
                print("Error fetching results from Google Speech Recognition; {0}".format(e))


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