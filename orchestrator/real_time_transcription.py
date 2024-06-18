import speech_recognition as sr
from circles_of_trust import CirclesOfTrust
import bulb_devices_functions

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
                        user = 'owner'
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
        'red': bulb_devices_functions.set_red,
        'blue': bulb_devices_functions.set_blue,
        'green': bulb_devices_functions.set_green,
        'yellow': bulb_devices_functions.set_yellow,
        'purple': bulb_devices_functions.set_purple,
        'orange': bulb_devices_functions.set_orange,
        'pink': bulb_devices_functions.set_pink,
        'indigo': bulb_devices_functions.set_indigo,
        'cyan': bulb_devices_functions.set_cyan,
        'magenta': bulb_devices_functions.set_magenta,
        'teal': bulb_devices_functions.set_teal,
        'lime': bulb_devices_functions.set_lime,
        'white': bulb_devices_functions.set_white_color,
        # 'increase saturation': bulb_devices_functions.increase_saturation,
        # 'decrease saturation': bulb_devices_functions.decrease_saturation,
        'brighten': bulb_devices_functions.increase_brightness,
        'dim': bulb_devices_functions.decrease_brightness
    }

    # tokenize the sentence
    words = sentence.lower().split()

    for word in words:
        if word in command_map:
            functionality = command_map[word]
            try:
                # Call the function directly
                access_control.execute_device_functionality('owner', functionality.__name__, 'light')
                print(f"Executed {functionality.__name__} for {'owner'}.")
            except ValueError as e:
                print(f"Failed to execute functionality: {e}")
