import re
from Logger import get_logger
import asyncio
from utils import *
from manga import ai
from cut import crop
from TTS import tts
import os
from Video import create_video
import glob

logger = get_logger("Main")

def _contains_alphabet(text):
    """Check if the given text contains any alphabetic character."""
    return any(char.isalpha() for char in text)

def get_Chapter_information(manga, Chapter):
    """Retrieve chapter pages and character data for the given manga and chapter."""
    logger.info(f"Processing manga: {manga}, Chapter: {Chapter}")
    Chapter_pages = load_chapter_in_manga(manga, Chapter)
    characters_data = get_characters_names("character_images")
    os.makedirs('temp', exist_ok=True)  # Ensure the temp directory exists
    return (Chapter_pages, characters_data)

def is_text_inside_panel(text, panel):
    """Check if a text box is fully contained within a panel."""
    x1_t, y1_t, x2_t, y2_t = text
    x1_p, y1_p, x2_p, y2_p = panel
    return x1_p <= x1_t and y1_p <= y1_t and x2_p >= x2_t and y2_p >= y2_t

def assign_texts_to_panels(panels, texts, ocr):
    """Assign detected text to their corresponding manga panels."""
    panel_texts = {i: [] for i in range(len(panels))}
    for text_idx, text in enumerate(texts):
        for panel_idx, panel in enumerate(panels):
            if is_text_inside_panel(text, panel):
                panel_texts[panel_idx].append(ocr[text_idx])
                break  # Stop checking once the text is assigned
    return panel_texts

async def main(manga, chapter):
    """Process the given manga chapter by analyzing and generating content."""
    Chapter_pages, characters_data = get_Chapter_information(manga, chapter)
    vid_index = 0
    
    # Sort the chapter pages based on numerical order extracted from filenames
    for index, page in enumerate(sorted(Chapter_pages, key=lambda x: int(re.search(r'(\d+)\.jpg$', os.path.basename(x)).group(1)))):
        logger.info(f"Processing page {index}/{len(Chapter_pages)}")
        dir = f'temp/{manga}/Chapter {chapter}/panel_{index}'
        os.makedirs(dir, exist_ok=True)
        
        logger.info(f"Running AI for page {index}")
        data = ai([str(page)], characters_data)[0]  # Run AI analysis on the page
        temp_panels = data['panels']  # Extract detected panels
        
        # Extract relevant OCR text
        ocr = [data['ocr'][i] for i in range(len(data['ocr'])) if data['is_essential_text'][i]]
        texts = [data['texts'][i] for i in range(len(data['texts'])) if data['is_essential_text'][i]]
        panel_text_mapping = assign_texts_to_panels(temp_panels, texts, ocr)
        
        # Process each detected panel
        for panel_idx, texts in panel_text_mapping.items():
            os.makedirs(f"{dir}/{panel_idx}", exist_ok=True)
            crop([temp_panels[panel_idx]], image_path=page, path=f"{dir}/{panel_idx}", panel_index=panel_idx)
        
        # Generate TTS audio for extracted texts
        for panel_idx, texts in panel_text_mapping.items():
            for i, text in enumerate(texts):
                if _contains_alphabet(text):  
                    await tts(text, saving_path=f"{dir}/{panel_idx}", index=i)
        
        # Generate videos combining cropped panels and corresponding TTS audio
        for panel_idx in range(len(temp_panels)):
            os.makedirs(f"temp/{manga}/Chapter {chapter}/video", exist_ok=True)
            create_video(
                glob.glob(f"{dir}/{panel_idx}/*.png")[0],  # Select the first cropped panel image
                glob.glob(f"{dir}/{panel_idx}/*.mp3"),  # Use corresponding TTS audio
                output_video=f"temp/{manga}/Chapter {chapter}/video/output_{vid_index}.mp4"
            )
            vid_index += 1

if __name__ == "__main__":
    # Get user input for manga name and chapter range
    manga = input("Enter the manga name: ")
    start_chapter = int(input("Enter the starting chapter: "))
    end_chapter = int(input("Enter the ending chapter: "))
    
    # Process chapters in the specified range
    for i in range(start_chapter, end_chapter + 1):
        asyncio.run(main(manga, i))