import edge_tts
import asyncio

async def tts(text: str, saving_path: str, index: int, voice: str = 'en-US-JennyNeural'):
    if not _contains_alphabet(text):
        return None
    tts = edge_tts.Communicate(text, voice=voice,rate="+25%",volume="+10%")
    # Save the speech as an MP3 file
    await tts.save(f"{saving_path}/{index}.mp3")
    
def _contains_alphabet(text):
    return any(char.isalpha() for char in text)
