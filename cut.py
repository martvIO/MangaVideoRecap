import cv2

# Load the image
image_path = "Manga/panel_1.png"  # Replace with your image path
image = cv2.imread(image_path)

# Define panel coordinates
panels = [
        [543.3638916015625, 703.1190185546875, 660.9219970703125, 814.8642578125]
]

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
    cv2.imwrite(f"panel_{i+1}.jpg", cropped)
    cv2.imshow(f"Panel {i+1}", cropped)

cv2.waitKey(0)
cv2.destroyAllWindows()
