import edge_tts
from Utils.Logger import get_logger
from Utils.utils import contains_alphabet

# Initialize the logger using the get_logger function
logger = get_logger("TTS")

async def tts(text: str, saving_path: str, index: int, voice: str = 'en-US-JennyNeural'):
    """
    This function converts the given text into speech and saves it as an MP3 file.
    
    Parameters:
    text (str): The text to be converted to speech.
    saving_path (str): The directory path where the MP3 file will be saved.
    index (int): An identifier for the audio file being generated (used for naming).
    voice (str): The voice model to use (default is 'en-US-JennyNeural').
    
    Returns:
    None: It saves the speech as an MP3 file in the specified location.
    """
    logger.info(f"Starting TTS for index {index} with voice '{voice}'")
    
    # Check if the text contains alphabetic characters, otherwise skip processing
    if not contains_alphabet(text):
        logger.warning(f"Text at index {index} does not contain any alphabetic characters. Skipping.")
        return None
    
    try:
        logger.info(f"Generating speech for text: '{text[:30]}...'")  # Logging first 30 chars of the text for preview
        # Create the TTS communication instance with the specified text and voice
        tts = edge_tts.Communicate(text, voice=voice, rate="+25%", volume="+10%")
        
        # Define the output file path for saving the MP3 file
        output_path = f"{saving_path}/{index}.mp3"
        logger.info(f"Saving speech to {output_path}")
        
        # Save the generated speech as an MP3 file
        await tts.save(output_path)
        
        # Log success after saving the file
        logger.info(f"Speech saved successfully at {output_path}")
    
    except Exception as e:
        # Log any errors that occur during the TTS process
        logger.error(f"An error occurred while generating speech for index {index}: {e}")
