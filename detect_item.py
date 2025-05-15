import cv2
import numpy as np
import json
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load checklist
with open("checklist.json", "r") as f:
    checklist = set(item.lower() for item in json.load(f))

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (512, 512))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    return Image.fromarray(enhanced)

def process_and_detect(image_path):
    image = preprocess_image(image_path)
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # Extract keywords from caption (very basic keyword split)
    detected_items = [word.strip().lower() for word in caption.replace('a ', '').replace('and', ',').split(',') if word.strip()]
    missing_items = list(checklist - set(detected_items))
    return detected_items, missing_items
