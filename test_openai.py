import openai
import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 從環境變數讀取 API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai():
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # ← 改這裡
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you confirm you're working?"}
        ]
    )

        print("✅ 測試成功！模型回應：")
        print(response['choices'][0]['message']['content'])
    except Exception as e:
        print("❌ 發生錯誤：")
        print(e)

if __name__ == "__main__":
    test_openai()
