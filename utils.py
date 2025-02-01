import os
from PIL import Image
import numpy as np
import glob

def find_text_panel_associations(panels, texts):
    text_panel_map = {}  # Store text index -> panel index mappings

    for text_idx, (x1_t, y1_t, x2_t, y2_t) in enumerate(texts):
        for panel_idx, (x1_p, y1_p, x2_p, y2_p) in enumerate(panels):
            # Check if text is inside the panel
            if x1_p <= x1_t and y1_p <= y1_t and x2_p >= x2_t and y2_p >= y2_t:
                text_panel_map[text_idx] = panel_idx
                break  # Assign the first matching panel and stop

    return text_panel_map

def read_image(path_to_image):
    with open(path_to_image, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    return image

def get_characters_names(path: str):
    characters = glob.glob(f"{path}/*")
    print(characters)
    names = [_get_filename(i) for i in characters]
    print(characters,names)

    data = {"images": characters,"names": names}
    return data

def load_chapter_in_manga(manga: str, chapter: int):
    paths = glob.glob(f"Manga/{manga}/Chapter {chapter}/*")
    return paths

def _get_filename(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]
if __name__ == "__main__":
    # Example Data (Panels and Texts)
    panels = [
        [70.32527923583984, -1.962268352508545, 751.8159790039062, 592.9677734375], 
        [71.09741973876953, 601.8713989257812, 762.0369262695312, 1198.671142578125]
    ]

    texts = [
            [313.5597839355469, 92.30513000488281, 390.0364990234375, 171.78257751464844], 
            [174.4681854248047, 133.69740295410156, 285.8901062011719, 252.25901794433594], 
            [671.6571655273438, 666.2120971679688, 703.3621826171875, 687.5729370117188], 
            [543.3638916015625, 703.1190185546875, 660.9219970703125, 814.8642578125], 
    ]

    # Calculate associations
    text_panel_associations = find_text_panel_associations(panels, texts)
    print(text_panel_associations)
    # Print results
    for text_idx, panel_idx in text_panel_associations.items():
        print(f"Text {text_idx} belongs to Panel {panel_idx}")
