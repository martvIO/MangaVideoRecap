import gradio as gr
import torch
from model import load_model
from utils import find_text_panel_associations, read_image
from Logger import get_logger
logger = get_logger(name="Manga")
import time
start = time.time()
model = load_model()
end = time.time()
logger.info(f"loading the model took: {end-start}")

def ai(chapter_pages, character_bank):
    chapter_pages = [read_image(x) for x in chapter_pages]
    character_bank["images"] = [read_image(x) for x in character_bank["images"] if isinstance(x, str)]

    with torch.no_grad():
        per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)  
    return per_page_results