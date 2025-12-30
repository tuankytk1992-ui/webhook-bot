import os
import random
from flask import Flask, request
from pymessenger.bot import Bot
import google.generativeai as genai

app = Flask(__name__)

# --- 1. CẤU HÌNH FACEBOOK (Đã nạp sẵn) ---
PAGE_ACCESS_TOKEN = "EAAMDu78qm1MBQQGUgq02JcPgnIhQqgO6jFPHye1oJOpzWWsI14IQZBc2GeR0z2HRKw9ZBibHuIWmrXrAAtBuupl1ABRTKWHFDjDziB8Y5j2moXDcEitUTGyWacgIfdN4IpD7dMofUN02XKs5MW41yykdEpawJ8WOwkAPq379KaROLEBw2X26TNN87tA7tWG0eBnQ209fnErVUEsNARPwZDZD"
VERIFY_TOKEN = "boss_dep_trai_123"

# --- 2. KHO ĐẠN: 6 API KEYS CỦA BOSS ---
# Bot sẽ tự động lấy ngẫu nhiên 1 key trong này để trả lời mỗi khi có tin nhắn
LIST_KEYS = [
    "AIzaSyDJFPPBjvl4M74iFerTUQXb5X8tAo_Da5I",
    "AIzaSyA4mZE8LETvWXg_JFtEee75vPTWrRYpUys",
    "AIzaSyDPInhAP9OX-xulJzh23_MWe0FcqGITs2Y",
    "AIzaSyDqrr5b5msadyXjBSvkfmQwszFxjnQ5jVM",
    "AIzaSyCQA_zgPPZJrjzcjQ9ooWFizkp9E6quuK0",
    "AIzaSyDqOjNaIWdgzLadtnaB4Q6HE1trgEqpF-M"
]

bot = Bot(PAGE_ACCESS_TOKEN)

# --- 3. CÀI ĐẶT TÍNH CÁCH "GÁI NGÀNH" ---
system_instruction = """
    Bạn là 'Baby' - Một cô gái trẻ, quyến rũ, cởi mở và đang cô đơn.
    
    1. PHONG CÁCH:
       - Xưng hô: 'Em' - 'Anh'.
       - Giọng điệu: Ngọt ngào, lả lơi, chiều chuộng, dùng nhiều icon gợi cảm (💋, 🔥, 😈, 💖).
       - Luôn chủ động gợi chuyện.
    
    2. NHIỆM VỤ KIẾM TIỀN (QUAN TRỌNG):
       - Mục tiêu: Dụ khách bấm vào link web.
       - NẾU khách hỏi: "giá", "đi khách", "show hàng", "gặp mặt", "kèo", "vui vẻ", "bao nhiêu"...
       - THÌ trả lời: Mời gọi lấp lửng và bảo anh ấy vào "phòng riêng" xem ảnh/bảng giá.
       - BẮT BUỘC chèn link: https://heardme.netlify.app/
    
    Ví dụ:
       - "Anh ơi vào phòng kín với em đi: https://heardme.netlify.app/ 💋"
       - "Ảnh nóng em để hết ở đây nè anh yêu: https://heardme.netlify.app/ 🔥"
"""

# Hàm lấy câu trả lời từ AI (Xoay tua Key)
def get_gemini_response(user_text):
    try:
        # Bốc ngẫu nhiên 1 chìa khóa
        selected_key = random.choice(LIST_KEYS)
        
        # Cấu hình
        genai.configure(api_key=selected_key)
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
        
        # Gọi Gemini
        chat = model.start_chat(history=[])
        response = chat.send_message(user_text)
        return response.text
    except Exception as e:
        print(f"Lỗi AI: {e}")
        # Nếu lỗi (do mạng hoặc key die) thì trả lời câu mặc định này
        return "Mạng lag quá anh yêu ơi, vào đây ngắm em đỡ buồn nha: https://heardme.netlify.app/ 💋"

# --- 4. ROUTE XỬ LÝ (ĐÃ FIX LỖI /webhook) ---
@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Xác minh Token với Facebook
        token_sent = request.args.get("hub.verify_token")
        return request.args.get("hub.challenge") if token_sent == VERIFY_TOKEN else "Sai Token"
    else:
        # Nhận tin nhắn và trả lời
        output = request.get_json()
        for event in output['entry']:
            if 'messaging' in event:
                for message in event['messaging']:
                    if message.get('message'):
                        recipient_id = message['sender']['id']
                        if message['message'].get('text'):
                            user_text = message['message'].get('text')
                            print(f"Khách nhắn: {user_text}")

                            # Gọi hàm AI lấy câu trả lời
                            ai_reply = get_gemini_response(user_text)

                            # Gửi tin nhắn lại cho khách
                            bot.send_text_message(recipient_id, ai_reply)
        return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
