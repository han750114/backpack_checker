import cv2
import numpy as np
import json
from PIL import Image
import torch
import openai
import os
import base64

# 讀入 checklist
with open("checklist.json", "r") as f:
    checklist = set(item.lower() for item in json.load(f))

# 讀取 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

# 改回彩圖處理

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (512, 512))
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# 對應詞典
translation_dict = {
    "pencil case": "pen",
    "sunglasses": "glasses",
    "compact pouch": "bag",
    "red zipper pouch": "bag",
    "blue striped pouch": "bag",
    "thermos bottle": "water bottle",
    "water bottle": "water bottle",
    "towel": "tissue",
    "card": "id card",
    "keys": "key",
    "keychain": "key",
    "hair ties": "accessory",
    "scrunchies": "accessory",
    "clothing": "clothes",
    "notebook": "notebook",
    "book": "notebook",
    "umbrella": "umbrella",
    "coin purse": "wallet",
    "wallet": "wallet",
    "lunchbox": "lunchbox",
    "packed lunch": "lunchbox",
    "phone": "phone",
    "mobile phone": "phone",
    "cellphone": "phone",
    "ruler": "ruler",
    "eraser": "eraser",
    "pen": "pen",
    "ballpoint pen": "pen"
}

# 主處理流程

def process_and_detect(image_path):
    image = preprocess_image(image_path)
    buffered = cv2.imencode(".jpg", np.array(image))[1].tobytes()
    base64_image = base64.b64encode(buffered).decode("utf-8")

    prompt = (
        "What objects do you clearly see inside this backpack? "
        "Please list them one per line without guessing. Skip unclear or hidden objects."
    )


    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant for identifying backpack contents from photos."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "auto"
                        }
                    }
                ]}
            ],
            max_tokens=500
        )

        caption = response.choices[0].message.content
        print("Generated Caption:", caption)

        with open("caption.txt", "w") as f:
            f.write(caption)

        raw_items = [line.strip().lower() for line in caption.split("\n") if line.strip() and any(c.isalnum() for c in line)]
        raw_items = [item.replace(".", "").replace(":", "").strip("-• ") for item in raw_items]

        normalized_items = set()
        for word in raw_items:
            word = word.lower()
            mapped = translation_dict.get(word, word)
            for checklist_item in checklist:
                if mapped in checklist_item or checklist_item in mapped:
                    normalized_items.add(checklist_item)
                    break

        missing_items = list(checklist - normalized_items)
        return list(normalized_items), missing_items

    except Exception as e:
        print("❌ 發生錯誤：", e)
        return [], list(checklist)
