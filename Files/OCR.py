import pytesseract
import os
import sys
from PIL import ImageGrab

tesseract_path = os.path.join(os.path.dirname(__file__), 'pytesseract', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

def capture(bbox):
    screenshot = ImageGrab.grab(bbox=bbox)
    return screenshot

def ocr(bbox, screenshot):
    try: 
        screenshot = screenshot.crop(bbox)
        # Take a screenshot of the specified bounding box

        # Use Tesseract to do OCR on the image and get bounding box information
        ocr_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        # Iterate through each word detected and draw them on the image
        for i in range(len(ocr_data['text'])):
            if int(ocr_data['conf'][i]) > 60:  # Confidence threshold
                (x, y, w, h) = (ocr_data['left'][i], ocr_data['top'][i], 
                                ocr_data['width'][i], ocr_data['height'][i])
                text = ocr_data['text'][i]
        try:
            return text
        except:
            return "Nothing Returned"

    except pytesseract.TesseractError as e:
        print(f"Tesseract Error: {e}", file=sys.stderr)
        return "OCR Failed"
    except Exception as e:
        print(f"General Error: {e}", file=sys.stderr)
        return "OCR Failed"