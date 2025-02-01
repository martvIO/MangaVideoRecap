import gradio as gr
from PIL import Image
import numpy as np
from transformers import AutoModel, AutoConfig
import torch
from utils import find_text_panel_associations
from Logger import get_logger
logger = get_logger(name="Manga")

model_name = "ragavsachdeva/magiv2" # this model is used to extract the text and the character's names from a manga panel

try:
    # loading the model from cache folder
    logger.info(f"trying to load the model {model_name} from the cache folder")
    model = AutoModel.from_pretrained(f"cache/model/{model_name}", trust_remote_code=True, force_download=True)
except: 
    logger.error(f"Failed to load the model {model_name} from the cache folder")
    # downloading the model from the huggingface model hub
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True, force_download=True)
    # saving the model in the cache/model folder
    model.save_pretrained(f"cache/model/{model_name}")
    logger.info(f"Model {model_name} saved to the cache folder")

logger.debug(f"load the model {model_name}")

def read_image(path_to_image):
    with open(path_to_image, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    return image

chapter_pages = ["Manga/panel_1.png"]
character_bank = {
    "images": ["character_images/Yuichiro Hyakuya.png", "character_images/Mika.jpeg"],
    "names": ["Yuichiro Hyakuya", "Mika"]
}

chapter_pages = [read_image(x) for x in chapter_pages]
character_bank["images"] = [read_image(x) for x in character_bank["images"]]

with torch.no_grad():
    per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)
    logger.debug(f"per_page_results: {per_page_results}")

data = per_page_results[0]
logger.debug(f"data: {data}")
panels = data['panels']
texts = [data['ocr'][i[0]] for i in data['text_tail_associations']]
print(panels,texts)
t = find_text_panel_associations(panels,texts)
logger.debug(f"t: {t}")
transcript = []
for i, (image, page_result) in enumerate(zip(chapter_pages, per_page_results)):
    model.visualise_single_image_prediction(image, page_result, f"page_{i}.png")
    speaker_name = {
        text_idx: page_result["character_names"][char_idx] for text_idx, char_idx in page_result["text_character_associations"]
    }
    for j in range(len(page_result["ocr"])):
        if not page_result["is_essential_text"][j]:
            continue
        name = speaker_name.get(j, "unsure") 
        transcript.append(f"<{name}>: {page_result['ocr'][j]}")
with open(f"transcript.txt", "w") as fh:
    for line in transcript:
        fh.write(line + "\n")    