import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Configure microphone settings
with sr.Microphone() as source:
    # Step 1: Calibrate for ambient noise (CRITICAL!)
    print("Calibrating for ambient noise... Please wait 2 seconds...")
    recognizer.adjust_for_ambient_noise(source, duration=2)

    # Step 2: Set energy threshold (adjust sensitivity)
    recognizer.energy_threshold = 4000  # Default is 300, increase if too sensitive
    recognizer.dynamic_energy_threshold = True  # Auto-adjust

    print("Say something now!")

    try:
        # Step 3: Better listen parameters
        audio = recognizer.listen(
            source,
            timeout=5,  # Wait 5 seconds for speech to start
            phrase_time_limit=10  # Maximum 10 seconds of speech
        )

        # Step 4: Try recognition with show_all for debugging
        print("Processing...")
        words = recognizer.recognize_google(audio)
        print(f" the words are : \n  {words}")



    except sr.WaitTimeoutError:
        print("No speech detected within 5 seconds.")
    except sr.UnknownValueError:
        print("Could not understand audio. Try speaking louder or clearer.")
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
    except Exception as e:
        print(f"Error: {e}")
