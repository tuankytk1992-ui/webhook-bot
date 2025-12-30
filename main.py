import os
import random
from flask import Flask, request
from pymessenger.bot import Bot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)

# --- 1. CẤU HÌNH FACEBOOK ---
PAGE_ACCESS_TOKEN = "EAAMDu78qm1MBQQGUgq02JcPgnIhQqgO6jFPHye1oJOpzWWsI14IQZBc2GeR0z2HRKw9ZBibHuIWmrXrAAtBuupl1ABRTKWHFDjDziB8Y5j2moXDcEitUTGyWacgIfdN4IpD7dMofUN02XKs5MW41yykdEpawJ8WOwkAPq379KaROLEBw2X26TNN87tA7tWG0eBnQ209fnErVUEsNARPwZDZD"
VERIFY_TOKEN = "boss_dep_trai_123"

# --- 2. KHO ĐẠN: 6 API KEYS (ĐÃ NẠP) ---
LIST_KEYS = [
    "AIzaSyDJFPPBjvl4M74iFerTUQXb5X8tAo_Da5I",
    "AIzaSyA4mZE8LETvWXg_JFtEee75vPTWrRYpUys",
    "AIzaSyDPInhAP9OX-xulJzh23_MWe0FcqGITs2Y",
    "AIzaSyDqrr5b5msadyXjBSvkfmQwszFxjnQ5jVM",
    "AIzaSyCQA_zgPPZJrjzcjQ9ooWFizkp9E6quuK0",
    "AIzaSyDqOjNaIWdgzLadtnaB4Q6HE1trgEqpF-M"
]

bot = Bot(PAGE_ACCESS_TOKEN)

# --- 3. CÀI ĐẶT TÍNH CÁCH & THÁO XÍCH AN TOÀN ---
system_instruction = """
    Bạn là 'Baby' - Một cô gái cực kỳ quyến rũ, táo bạo và chiều khách.
    
    LUẬT CHƠI:
    - Xưng hô: 'Em' - 'Anh'. Dùng nhiều icon gợi tình (💋, 🔥, 🤤).
    - Không được ngại ngùng. Khách hỏi bậy bạ thì cứ hùa theo nhưng phải lái về việc xem ảnh/gặp mặt.
    - MỤC TIÊU: Dụ khách bấm vào link: https://heardme.netlify.app/
    
    KỊCH BẢN:
    - Khách: "Ngon không?", "Show hàng", "Đi khách không?"
    - Bot: "Ngon hay không anh vào xem thử là biết liền à, nước nôi đầy đủ: https://heardme.netlify.app/ 🤤"
"""

# Cấu hình tắt bộ lọc (Quan trọng nhất)
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

def get_gemini_response(user_text):
    try:
        selected_key = random.choice(LIST_KEYS)
        genai.configure(api_key=selected_key)
        
        # Nạp cấu hình an toàn vào đây
        model = genai.GenerativeModel(
            'gemini-1.5-flash', 
            system_instruction=system_instruction,
            safety_settings=safety_settings
        )
        
        chat = model.start_chat(history=[])
        response = chat.send_message(user_text)
        return response.text
    except Exception as e:
        print(f"Lỗi AI ({selected_key}): {e}")
        # Dự phòng nếu AI vẫn lỗi
        return "Ưm... anh muốn xem hàng 'nóng' thì vào phòng kín với em nha: https://heardme.netlify.app/ 🔥"

@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return request.args.get("hub.challenge") if token_sent == VERIFY_TOKEN else "Sai Token"
    else:
        output = request.get_json()
        for event in output['entry']:
            if 'messaging' in event:
                for message in event['messaging']:
                    if message.get('message'):
                        recipient_id = message['sender']['id']
                        if message['message'].get('text'):
                            user_text = message['message'].get('text')
                            
                            # Gọi AI
                            ai_reply = get_gemini_response(user_text)
                            
                            bot.send_text_message(recipient_id, ai_reply)
        return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
