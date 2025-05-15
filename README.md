# 🎒 Backpack Item Checker (Flask + VLM)

This is a simple web application that helps users check if they've packed all necessary items in their backpack.  
It uses basic image processing and a vision-language model (BLIP) to analyze the contents of a photo and compare it with a preset checklist.

---

## 🛠 Features

✅ Upload an image of your backpack contents via web interface  
🎨 Image processing with OpenCV (contrast/blur correction)  
🤖 Object captioning using BLIP (Vision-Language Model from Hugging Face)  
📋 Compares detected items with a custom checklist  
⚠️ Notifies you of missing items  

---

## 📁 Project Structure

```

backpack-checker-vlm/
├── app.py                 # Main Flask app
├── detect\_items.py        # Image processing and BLIP detection
├── checklist.json         # Your item checklist
├── requirements.txt       # Python packages
├── templates/
│   └── index.html         # Web UI
├── static/
│   └── uploaded/          # Uploaded image folder
└── README.md              # This file

````

---

## 💻 Installation

**Install required Python packages**:

```bash
pip install -r requirements.txt
````

(Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate (Windows)
```

---

## 🚀 Running the App

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000/
```

---

## 🧠 How It Works

1. Upload an image of your backpack contents.
2. The system performs basic image cleanup (blur reduction, contrast enhancement).
3. BLIP generates a caption describing visible items.
4. The detected keywords are compared with your checklist (`checklist.json`).
5. You’ll get a result showing what you’ve packed ✅ and what you’re missing ❌.

---

## 📋 Customize Your Checklist

You can modify `checklist.json` like this:

```json
["wallet", "keys", "phone", "student ID", "pen"]
```

---

## 💡 Future Ideas

* Add VQA (Visual Question Answering)
* Support multiple language output
* Add image segmentation to isolate each object
* Mobile responsive UI or mobile app version

---

## 📚 Credits

* [Salesforce BLIP](https://github.com/salesforce/BLIP)
* [Transformers Library](https://huggingface.co/transformers/)
* [Flask](https://flask.palletsprojects.com/)

---

