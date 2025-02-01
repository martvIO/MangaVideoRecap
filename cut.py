import cv2, os

def crop(panels, image_path: str, path: str, panel_index:int):  # Replace with your image path
    os.makedirs(path,exist_ok=True)
    image = cv2.imread(image_path)
    # Convert float to integers for slicing
    panels = [[int(x) for x in panel] for panel in panels]

    z = 50
    # Crop and save each panel
    for i, (x1, y1, x2, y2) in enumerate(panels):
        # Ensure coordinates are within the image bounds
        y1, y2 = max(0, y1-z), min(image.shape[0], y2+z)
        x1, x2 = max(0, x1-z), min(image.shape[1], x2+z)

        # Crop the image
        cropped = image[y1:y2, x1:x2]

        # Save or display
        cv2.imwrite(f"{path}/{panel_index}.png", cropped)
        cv2.imshow(f"{path}/{panel_index}.png", cropped)
