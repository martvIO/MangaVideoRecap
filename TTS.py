import edge_tts
import asyncio

async def main(text: str, saving_path: str, index: int, voice: str = 'en-US-EmilyV3Voice'):
    tts = edge_tts.Communicate(text, voice=voice)
    
    # Save the speech as an MP3 file
    await tts.save(f"{saving_path}/{index}.mp3")

