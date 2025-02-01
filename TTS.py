import edge_tts
import asyncio

async def main(text: str, character_name: str,index: int):
    tts = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    
    # Save the speech as an MP3 file
    await tts.save(f"{character_name}_{index}.mp3")

# Run the async function
asyncio.run(main())
