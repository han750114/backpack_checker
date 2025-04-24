# vision_llm_project

This is a simple web application built with Flask. It allows users to upload an image, processes the image using basic computer vision, and sends the result to OpenAI GPT for semantic analysis.



## 🛠️ Features

- ✅ Upload an image through a browser interface  
- 🖼️ Process the image with OpenCV / Pillow  
- 🤖 Use OpenAI GPT API for text-based analysis  
- 🌐 Handle API requests and responses  



## 📦 Installation

> ⚠️ You are **not** using a virtual environment.  
> The following commands will install dependencies **globally** on your system.

Install required Python packages:
```bash
pip3 install -r requirements.txt
```

If needed (e.g. permission error):
```bash
sudo pip3 install -r requirements.txt
```



## 📁 Project Structure

```
project-root/
├── app.py               # Main Flask application
├── templates/
│   └── index.html       # Web page for image upload
├── static/
│   └── uploaded/        # Folder to store uploaded images
├── requirements.txt     # List of Python packages
├── .env                 # Contains your OpenAI API key
└── README.md            # This file
```



## 🚀 Running the App

Start the Flask development server:

```bash
python3 app.py
```

Open your browser and visit:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)



## 🔐 .env File

Create a `.env` file in the project root to store your API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```



## 💡 Future Ideas

- 🧠 Add object detection (e.g. YOLOv8)  
- 📝 Generate image captions or Q&A with ChatGPT  
- ☁️ Deploy to a cloud platform (Heroku, Render, etc.)  
- 🎨 Improve UI with Bootstrap or Vue/React  


```