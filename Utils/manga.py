import torch
from Utils.model import load_model
from Utils.utils import read_image
from Utils.Logger import get_logger
import time

# Initialize logger for tracking the AI process
logger = get_logger(name="Manga")

# Measure the time it takes to load the model
start = time.time()
logger.info("Loading the model...")
model = load_model()  # Load the model using the load_model function
end = time.time()
logger.info(f"Loading the model took: {end - start:.2f} seconds.")  # Log the time taken to load the model

def ai(chapter_pages, character_bank):
    """
    This function processes the input images and character bank, running the AI model to make predictions.
    
    It reads the manga chapter pages and character bank images, then runs a model prediction on them.
    The results per page are returned as a result.

    Args:
    - chapter_pages (list): List of paths to chapter pages (images).
    - character_bank (dict): Dictionary containing a list of character images.

    Returns:
    - per_page_results: Results from the model prediction for each page.
    """
    
    # Read the images of the chapter pages
    logger.info("Reading chapter pages...")
    chapter_pages = [read_image(x) for x in chapter_pages]
    logger.debug(f"Processed {len(chapter_pages)} chapter pages.")

    # Read the images of the character bank
    logger.info("Reading character bank images...")
    character_bank["images"] = [read_image(x) for x in character_bank["images"] if isinstance(x, str)]
    logger.debug(f"Processed {len(character_bank['images'])} character images.")

    # Perform prediction using the model (no gradients needed)
    logger.info("Running the model for chapter-wide predictions...")
    with torch.no_grad():
        per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)  
    
    # Log that the prediction is completed
    logger.info("Model prediction completed.")
    return per_page_results
