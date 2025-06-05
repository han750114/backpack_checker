import os
import cv2
import openai
import numpy as np
from PIL import Image
import base64

# ✅ 設定 OpenAI API 金鑰（請確保已在環境變數中設定 OPENAI_API_KEY）
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ 模擬一份預期物品清單（可換成從檔案讀取）
EXPECTED_ITEMS = [
    "book", "notebook", "sunglasses", "water bottle", "pencil case",
    "umbrella", "wallet", "keychain", "snack", "towel", "card"
]

# ✅ CLAHE 增強對比 + 邊緣偵測 + 輪廓裁切
def extract_objects(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # CLAHE 對比增強
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # 邊緣偵測 + 輪廓
    edges = cv2.Canny(enhanced, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    crops = []
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 10000:  # 過濾太小的雜訊框
            crop = image[y:y+h, x:x+w]
            crop_path = f"static/uploaded/crop_{i}.jpg"
            cv2.imwrite(crop_path, crop)
            crops.append(crop_path)
    return crops

# ✅ 將單一圖片轉 base64 並送 GPT 生成描述
def describe_image(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    base64_img = base64.b64encode(image_data).decode("utf-8")

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that identifies objects in cropped images from a backpack."},
                {"role": "user", "content": [
                    {"type": "text", "text": "What object is shown in this cropped photo? Be concise."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(Error: {str(e)})"

# ✅ 完整流程整合

def process_and_detect_b(image_path):
    object_crops = extract_objects(image_path)
    crop_results = [describe_image(p) for p in object_crops]

    # 比對有無缺項（只簡單字串比對，可改進）
    found = set()
    for caption in crop_results:
        for item in EXPECTED_ITEMS:
            if item.lower() in caption.lower():
                found.add(item)
    missing_items = [item for item in EXPECTED_ITEMS if item not in found]

    return list(found), missing_items, object_crops, crop_results
