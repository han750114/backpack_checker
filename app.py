from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['image']  # 取得上傳的圖片
    # 在這裡處理圖片（如物件偵測）
    return jsonify({"message": "圖片上傳成功！"})

if __name__ == '__main__':
    app.run(debug=True)
