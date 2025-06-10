import os
import cv2
import openai
import numpy as np
import base64
from PIL import Image
from datetime import datetime

# 設定 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

# 預期物品清單
EXPECTED_ITEMS = [
    "book", "notebook", "sunglasses", "water bottle", "pencil case",
    "umbrella", "wallet", "keychain", "snack", "towel", "card"
]

def extract_backpack_region(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")

    scale_width = 600
    h, w = img.shape[:2]
    scale = scale_width / w
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    img_rgb = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    edges = cv2.Canny(blurred, 86, 150)
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=3)
    edges = cv2.erode(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    backpack_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            backpack_cnt = cnt

    if backpack_cnt is None:
        return None

    x, y, w, h = cv2.boundingRect(backpack_cnt)
    return img[y:y+h, x:x+w]

def describe_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    base64_img = base64.b64encode(buffer).decode("utf-8")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that identifies objects in cropped images from a backpack."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "List all the objects show in backback in this cropped photo? Be concise."},
                        #{"type": "text", "text": "What object is shown in this cropped photo? Be concise."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]
                }
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(Error: {str(e)})"

def process_and_detect_b(image_path):
    cropped_backpack = extract_backpack_region(image_path)
    if cropped_backpack is None:
        return [], EXPECTED_ITEMS, [], os.path.basename(image_path)

    # 儲存裁剪後圖像
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    crop_filename = f"backpack_crop_{timestamp}.jpg"
    crop_path = os.path.join("static", "uploaded", crop_filename)
    cv2.imwrite(crop_path, cropped_backpack)

    caption = describe_image(cropped_backpack)
    found = []
    for item in EXPECTED_ITEMS:
        if item.lower() in caption.lower():
            found.append(item)
    missing = [item for item in EXPECTED_ITEMS if item not in found]

    return found, missing, [(crop_filename, caption)], os.path.basename(image_path)
