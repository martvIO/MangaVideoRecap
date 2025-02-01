import gradio as gr
import torch
from model import load_model
from utils import find_text_panel_associations, read_image
from Logger import get_logger
logger = get_logger(name="Manga")

model = load_model()

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
texts = [data['texts'][i[0]] for i in data['text_tail_associations']]
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