from Logger import get_logger
import asyncio
from utils import *
from manga import ai
from cut import crop
from TTS import tts
import os
from Video import create_video
def _contains_alphabet(text):
    return any(char.isalpha() for char in text)

logger = get_logger("Main")
manga = "Seraph of the end"

# Log the start of the process
logger.info(f"Processing manga: {manga}")

# Getting chapter panels
logger.info("Getting chapter panels for the first chapter")
Chapter_pages = load_chapter_in_manga(manga, 1)

# Load character data
logger.info("Loading character data")
characters_data = get_characters_names("character_images")

# Create temporary directory for storing files
os.makedirs('temp', exist_ok=True)
async def main():
    # Process each page in the chapter
    for index, page in enumerate(Chapter_pages):
        logger.info(f"Processing page {index + 1}/{len(Chapter_pages)}")

        # Create directory for the current page
        dir = f'temp/{manga}/panel_{index}'
        os.makedirs(dir, exist_ok=True)

        # Analyze page using AI
        logger.info(f"Running AI for page {index + 1}")
        data = ai([page], characters_data)[0]
        logger.debug(f"AI analysis data: {data}")

        # Extract panel information
        temp_panels = data['panels']

        # Extract associated texts
        texts = [data['texts'][i[0]] for i in data['text_tail_associations']]
        logger.debug(f"Texts associated with panels: {texts}")

        print(temp_panels, texts)

        # Find text-panel associations
        logger.info(f"Finding text-panel associations for page {index + 1}")
        t = find_text_panel_associations(temp_panels, texts)
        logger.debug(f"Text-panel associations: {t}")

        x = []
        j = 0
        for i in range(len(data['texts'])):
            print(i)
            if len(texts) == j:
                break
            if data['texts'][i] == texts[j]:
                y = [i, t[j]]
                x.append(y) 
                j += 1
        logger.debug(f"Text-panel pairings: {x}")

        print(x)

        logger.info(f"Cropping panels for page {index + 1}")
        for i in range(len(x)):
            os.makedirs(f"{dir}/{x[i][1]}",exist_ok=True)
            logger.debug(temp_panels[x[i][1]])
            print([temp_panels[x[i][1]]],page,f"{dir}/{x[i][1]}",x[i][1])
            crop([temp_panels[x[i][1]]], image_path=page, path=f"{dir}/{x[i][1]}", panel_index=x[i][1])

        # Generate audio for each text associated with a panel
        for i in x:
            panel_index = i[1]
            text_index = i[0]
            text = data['ocr'][text_index]
            logger.info(f"Generating audio for text: {text} (Panel: {panel_index}, Text Index: {text_index})")
            if _contains_alphabet(text):  
                await tts(text, saving_path=f"{dir}/{i[1]}",index=text_index)
        
        for i in get_all_directories(dir):
            print(get_all_directories(dir))
            print(glob.glob(f"{i}/*.png"),glob.glob(f"{i}/*.mp3"))
            create_video(glob.glob(f"{i}/*.png"),glob.glob(f"{i}/*.mp3"),output_video=f"{i}/{"output"}")
logger.info("Processing complete")
# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())