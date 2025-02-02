from Logger import get_logger
import asyncio
from utils import *
from manga import ai
from cut import crop
from TTS import tts
import os
from Video import create_video, combine_videos
import glob

def _contains_alphabet(text):
    return any(char.isalpha() for char in text)

logger = get_logger("Main")
manga = "Seraph of the end"
Chapter = 1
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

# Define the helper functions here

def is_text_inside_panel(text, panel):
    """Check if a text box is fully inside a panel."""
    x1_t, y1_t, x2_t, y2_t = text
    x1_p, y1_p, x2_p, y2_p = panel
    return x1_p <= x1_t and y1_p <= y1_t and x2_p >= x2_t and y2_p >= y2_t


def assign_texts_to_panels(panels, texts, ocr):
    """Assign text boxes to their corresponding panels."""
    panel_texts = {i: [] for i in range(len(panels))}  # Dictionary to store text per panel
    
    for text_idx, text in enumerate(texts):
        for panel_idx, panel in enumerate(panels):
            if is_text_inside_panel(text, panel):
                panel_texts[panel_idx].append(ocr[text_idx])  # Store the text content
                break  # Stop checking once the text is assigned to a panel
    
    return panel_texts

async def main():
    # Process each page in the chapter
    for index, page in enumerate(Chapter_pages):
        logger.info(f"Processing page {index}/{len(Chapter_pages)}")

        # Create directory for the current page
        dir = f'temp/{manga}/Chapter {Chapter}/panel_{index}'
        os.makedirs(dir, exist_ok=True)

        # Analyze page using AI
        logger.info(f"Running AI for page {index}")
        print([str(page)])
        data = ai([str(page)], characters_data)[0]
        logger.debug(f"AI analysis data: {data}")

        # Extract panel and text information
        temp_panels = data['panels']
        ocr = [data['ocr'][i] for i in range(len(data['ocr'])) if data['is_essential_text'][i]]
        texts = [data['texts'][i] for i in range(len(data['texts'])) if data['is_essential_text'][i]]

        # Assign texts to their corresponding panels using the function
        logger.info(f"Assigning texts to panels for page {index}")
        panel_text_mapping = assign_texts_to_panels(temp_panels, texts, ocr)
        logger.debug(f"Text-panel mapping: {panel_text_mapping}")

        # Now you have a dictionary `panel_text_mapping` that links each panel to the text(s) inside it.
        # You can process the panels and texts as needed (e.g., cropping, TTS).

        for panel_idx, texts in panel_text_mapping.items():
            logger.info(f"Processing Panel {panel_idx}")
            # Crop the panel (optional step, depending on your needs)
            os.makedirs(f"{dir}/{panel_idx}",exist_ok=True)
            crop([temp_panels[panel_idx]], image_path=page, path=f"{dir}/{panel_idx}", panel_index=panel_idx)

        for panel_idx, texts in panel_text_mapping.items():
            logger.info(f"Processing Panel {panel_idx}")
            # Process each text inside this panel
            for i,text in enumerate(texts):
                logger.info(f"Generating audio for text: {text} (Panel: {panel_idx})")
                if _contains_alphabet(text):  
                    await tts(text, saving_path=f"{dir}/{panel_idx}", index=i)

        # Generate videos for each panel (after cropping and TTS)
        for panel_idx in range(len(temp_panels)):
            logger.info(f"Creating video for Panel {panel_idx}")
            create_video(
                glob.glob(f"{dir}/{panel_idx}/*.png")[0], 
                glob.glob(f"{dir}/{panel_idx}/*.mp3"), 
                output_video=f"{dir}/{panel_idx}/output.mp4"
            )

        combine_videos(f"{dir}", f"{dir}/combined_{index}.mp4")
    combine_videos(f"temp/{manga}/Chapter {Chapter}", f"{dir}/combined_{Chapter}.mp4")

logger.info("Processing complete")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
