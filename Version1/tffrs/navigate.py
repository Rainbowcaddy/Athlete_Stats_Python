import pyautogui
import cv2
import pytesseract
from PIL import Image

# Step 1: Capture the screen
screenshot = pyautogui.screenshot()
screenshot.save('screen.png')

# Step 2: Process the image for better text recognition
image = cv2.imread('screen.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the processed image
cv2.imshow('Processed Image', gray_image)
cv2.waitKey(0)  # Wait for a key press to close
cv2.destroyAllWindows()

# Step 3: Use Tesseract to recognize text
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Path to tesseract executable
text_data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)

# Step 4: Find the coordinates of "Shot" and "Put" text
shot_x, shot_y, shot_w, shot_h = None, None, None, None
put_x, put_y, put_w, put_h = None, None, None, None

for i in range(len(text_data['text'])):
    if "shot" in text_data['text'][i].lower():
        shot_x, shot_y, shot_w, shot_h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
    if "put" in text_data['text'][i].lower():
        put_x, put_y, put_w, put_h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]

# Optional: Debugging - Print recognized text
print(text_data['text'])

# Step 5: Check if "Shot" and "Put" are close enough and then click
if shot_x is not None and put_x is not None:
    # Define a threshold for how close they should be (e.g., 50 pixels)
    if abs(shot_x - put_x) < 50 and abs(shot_y - put_y) < 50:
        x = (shot_x + put_x) / 2
        y = (shot_y + put_y) / 2
        pyautogui.moveTo(x, y)
        pyautogui.click()
    else:
        print("Text 'shot put' not found close enough on the screen.")
else:
    print("Text 'shot put' not found on the screen.")
