# Backpack Item Checker

This is a simple web app that uses OpenAI's GPT-4o with vision to recognize items inside a backpack based on an uploaded image. It compares the detected items with a predefined checklist and highlights which items are detected and which are missing.

## ✅ Features
- Upload a backpack image via browser
- Automatically resize and encode the image
- Use OpenAI GPT-4o to analyze image contents
- Compare detected items against a checklist
- Display results with missing items highlighted

## 📁 Project Structure
```
backpack_checker/
├── app.py                  # Flask server
├── detect_item.py         # Main image + GPT-4o processing logic
├── checklist.json         # Predefined list of required items
├── templates/
│   └── index.html         # Upload and result page
├── static/
│   └── uploaded/          # Uploaded image folder
├── .env                   # (optional) Contains OpenAI API key
├── requirements.txt       # Python package list
└── README.md              # This file
```

## 📦 Installation
```bash
pip install -r requirements.txt
```

If you're using a `.env` file:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

## 🚀 Run the App
```bash
python app.py
```
Visit: `http://127.0.0.1:5000/`

## 🧠 How It Works
- The image is resized to 384x384 and base64 encoded
- It is passed to OpenAI GPT-4o with a clear visual prompt
- The response is parsed line-by-line and compared to a checklist
- Any unmatched items are considered "missing"

---
MIT License © 2025
