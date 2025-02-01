import gradio as gr
from PIL import Image
import numpy as np
from transformers import AutoModel, AutoConfig
import torch
import spaces
import os

model = AutoModel.from_pretrained("ragavsachdeva/magiv2", trust_remote_code=True, force_download=True)
model = model.cuda().eval()

def read_image(image):
    image = Image.open(image).convert("L").convert("RGB")
    image = np.array(image)
    return image

def process_images(chapter_pages, character_bank_images, character_bank_names):
    if chapter_pages is None:
        return [], ""
    if character_bank_images is None:
        character_bank_images = []
        character_bank_names = "" 
    if character_bank_names is None or character_bank_names == "":
        character_bank_names = ",".join([os.path.splitext(os.path.basename(x))[0] for x in character_bank_images])
    chapter_pages = [read_image(image) for image in chapter_pages]
    character_bank = {
        "images": [read_image(image) for image in character_bank_images],
        "names": character_bank_names.split(",")
    }

    with torch.no_grad():
        per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)

    # Create the 'image_temp' directory if it doesn't exist
    output_dir = 'image_temp'
    os.makedirs(output_dir, exist_ok=True)

    output_images = []
    transcript = []
    for i, (image, page_result) in enumerate(zip(chapter_pages, per_page_results)):
        output_image = model.visualise_single_image_prediction(image, page_result, filename=None)
        output_images.append(output_image)
        
        output_image_path = os.path.join(output_dir, f"output_image_{i+1}.png")
        Image.fromarray(output_image).save(output_image_path)
        speaker_name = {
            text_idx: page_result["character_names"][char_idx] for text_idx, char_idx in page_result["text_character_associations"]
        }
        temp = []    
        start = len(transcript)-1
        for j in range(len(page_result["ocr"])):
            if not page_result["is_essential_text"][j]:
                continue
            name = speaker_name.get(j, "unkown") 
            transcript.append(f"{name}: {page_result['ocr'][j]}")
            temp.append(f"{name}: {page_result['ocr'][j]}")
        
        #Save transcript text for each page in tmp directory
        with open(f"tmp/page_{i+1}_transcript.txt", "a") as file:
            for j in range(len(temp)):
                file.write(temp[j]+"\n")

    transcript_text = "\n".join(transcript)
    print(transcript_text)
    return output_images, transcript_text

images = list_ordered_image_paths("serpah_of_the_end")
character_bank_images = get_all_files("character_images")
print(character_bank_images)
process_images(images,character_bank_images,None)