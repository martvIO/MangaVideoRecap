import os
from PIL import Image
import numpy as np
import glob
from Utils.Logger import get_logger

# Set up the logger
logger = get_logger("utils")

def read_image(path_to_image):
    logger.info(f"Reading image from: {path_to_image}")
    with open(path_to_image, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    logger.info(f"Image read and converted to array.")
    return image

def get_characters_names(path: str):
    logger.info(f"Fetching character names from directory: {path}")
    characters = glob.glob(f"{path}/*")
    logger.debug(f"Found characters: {characters}")
    names = [_get_filename(i) for i in characters]
    logger.debug(f"Character names: {names}")

    data = {"images": characters, "names": names}
    logger.info("Character names fetched successfully.")
    return data

def load_chapter_in_manga(manga: str, chapter: int):
    logger.info(f"Loading paths for manga: {manga}, chapter: {chapter}")
    paths = glob.glob(f"Manga/{manga}/Chapter {chapter}/*")
    logger.info(f"Loaded {len(paths)} paths for chapter {chapter}.")
    return paths

def _get_filename(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

def get_all_directories(path):
    logger.info(f"Getting all directories in path: {path}")
    # List all items in the given directory
    all_items = os.listdir(path)
    
    # Filter and return only the directories
    directories = [item for item in all_items if os.path.isdir(os.path.join(path, item))]
    
    logger.info(f"Found {len(directories)} directories.")
    return directories

def contains_alphabet(text):
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