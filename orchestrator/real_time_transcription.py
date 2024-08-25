import speech_recognition as sr

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
        # light commands
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
        # plug commands
        'off': 'plug_off',
        'on': 'plug_on',
        # device commands (adding)
        'add device': 'add_device',
        'remove device': 'remove_device',
        'add user': 'add_user',
        'remove user': 'remove_user',
        'add user circle': 'add_user_to_circle',
        'remove user circle': 'remove_user_from_circle',
        'add device circle': 'add_device_to_trust_level',
        'remove device circle': 'remove_device_trust_level'
    }

    light_functionalities = {
        'set_red', 'set_blue', 'set_green', 'set_yellow', 'set_purple',
        'set_orange', 'set_pink', 'set_indigo', 'set_cyan', 'set_magenta',
        'set_teal', 'set_lime', 'set_white_color', 'increase_brightness',
        'decrease_brightness'
    }

    plug_functionalities = {'plug_off', 'plug_on'}

    trust_levels = {'trusted', 'partially trusted', 'untrusted'}

    device_types = {'light', 'plug'}

    # Tokenize the sentence
    words = sentence.lower().split()

    functionality_name = None
    detected_device_type = None
    for word in words:
        if word in command_map:
            functionality_name = command_map[word]

            # Determine the device type based on the functionality name
            if functionality_name in light_functionalities:
                detected_device_type = 'light'
            elif functionality_name in plug_functionalities:
                detected_device_type = 'plug'

            if functionality_name == 'add_device':
                device_name = words[-1]  # Or any logic to identify the device name
                functionalities = []
                device_instance = None
                access_control.add_device(device_name, functionalities, device_instance)
                print(f"Device '{device_name}' added for user '{user}'.")
                return

            elif functionality_name == 'remove_device':
                device_name = words[-1]  # Simplified assumption
                access_control.remove_device(device_name)
                print(f"Device '{device_name}' removed.")
                return

            elif functionality_name == 'add_user':
                new_user = words[-1]  # Simplified assumption
                access_control.add_user(new_user)
                print(f"User '{new_user}' added.")
                return

            elif functionality_name == 'add_user_to_circle':
                circle_name = words[-1]  # Simplified assumption
                access_control.add_user_to_circle(user, circle_name)
                print(f"User '{user}' added to circle '{circle_name}'.")
                return

            elif functionality_name == 'remove_user_from_circle':
                circle_name = words[-1]  # Simplified assumption
                access_control.remove_user_from_circle(user, circle_name)
                print(f"User '{user}' removed from circle '{circle_name}'.")
                return

            elif functionality_name == 'add_device_to_trust_level':
                trust_level = next((word for word in words if word in trust_levels), None)
                device_name = next((word for word in words if word in device_types), None)
                functionalities = []  # Define functionalities
                device_instance = None  # Instantiate or retrieve the device instance
                if trust_level and device_name:
                    access_control.add_device_to_trust_level(trust_level, device_name, functionalities, device_instance)
                    print(f"Device '{device_name}' added to trust level '{trust_level}'.")
                return

            elif functionality_name == 'remove_device_from_trust_level':
                trust_level = next((word for word in words if word in trust_levels), None)
                device_name = next((word for word in words if word in device_types), None)
                if trust_level and device_name:
                    access_control.remove_device_from_trust_level(trust_level, device_name)
                    print(f"Device '{device_name}' removed from trust level '{trust_level}'.")
                return

            else:
                device_type = 'unknown'

            try:
                # Execute the device functionality
                access_control.execute_device_functionality(user, functionality_name, detected_device_type)
                print(f"Executed {functionality_name} for {user}.")
            except ValueError as e:
                print(f"Failed to execute functionality: {e}")

            break  # Stop processing after the first valid command
        else:
            print(f"No valid command found in: {sentence}")
