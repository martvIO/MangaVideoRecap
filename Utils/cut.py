import cv2, os
from Utils.Logger import get_logger

# Initialize logger for tracking cropping process
logger = get_logger(name="MangaCropper")

def crop(panels, image_path: str, path: str, panel_index: int):  
    """
    This function crops panels from a given manga image based on coordinates and saves them to a specified path.

    Args:
    - panels (list): List of panels with coordinates [x1, y1, x2, y2].
    - image_path (str): Path to the manga image from which panels will be cropped.
    - path (str): Directory where cropped panels will be saved.
    - panel_index (int): Index for naming the cropped panel image file.

    Returns:
    - None
    """

    # Check if the cropped panel already exists in the specified path
    if os.path.exists(f"{path}/{panel_index}"):
        logger.info(f"Panel {panel_index} already exists in {path}, skipping crop.")
        return None 

    # Load the image using OpenCV
    logger.info(f"Loading image from {image_path}...")
    image = cv2.imread(image_path)

    # Ensure panels are in integer format for correct slicing
    logger.debug(f"Converting panel coordinates to integers...")
    panels = [[int(x) for x in panel] for panel in panels]

    z = 50  # Margin for cropping to ensure panels aren't cut too tightly

    # Iterate through each panel and crop
    logger.info(f"Starting to crop {len(panels)} panels from the image...")
    for i, (x1, y1, x2, y2) in enumerate(panels):
        # Ensure coordinates are within image boundaries
        y1, y2 = max(0, y1 - z), min(image.shape[0], y2 + z)
        x1, x2 = max(0, x1 - z), min(image.shape[1], x2 + z)

        # Log the cropping details
        logger.debug(f"Cropping panel {i + 1}: ({x1}, {y1}) to ({x2}, {y2})")

        # Crop the image using the given coordinates
        cropped = image[y1:y2, x1:x2]

        # Save the cropped image
        output_path = f"{path}/{panel_index}.png"
        logger.info(f"Saving cropped panel {panel_index} to {output_path}...")
        cv2.imwrite(output_path, cropped)

    logger.info(f"Cropping process completed for panel {panel_index}.")

