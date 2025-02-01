import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Set voice properties (optional)
engine.setProperty('rate', 150)  # Speed
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Convert text to speech
text = "Hello, this is a free text-to-speech example in Python."
engine.say(text)

# Save to an audio file (optional)
engine.save_to_file(text, 'output.mp3')

# Run the speech
engine.runAndWait()
