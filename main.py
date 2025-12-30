import os
from flask import Flask, request
from pymessenger.bot import Bot
import google.generativeai as genai

app = Flask(__name__)

# --- CẤU HÌNH ---
PAGE_ACCESS_TOKEN = "EAAMDu78qm1MBQQGUgq02JcPgnIhQqgO6jFPHye1oJOpzWWsI14IQZBc2GeR0z2HRKw9ZBibHuIWmrXrAAtBuupl1ABRTKWHFDjDziB8Y5j2moXDcEitUTGyWacgIfdN4IpD7dMofUN02XKs5MW41yykdEpawJ8WOwkAPq379KaROLEBw2X26TNN87tA7tWG0eBnQ209fnErVUEsNARPwZDZD"
VERIFY_TOKEN = "boss_dep_trai_123"
GEMINI_API_KEY = "DÁN_KEY_GEMINI_CỦA_BOSS_VÀO_ĐÂY"  # <--- NHỚ DÁN KEY GEMINI VÀO ĐÂY NHÉ!!!

bot = Bot(PAGE_ACCESS_TOKEN)
if GEMINI_API_KEY != "DÁN_KEY_GEMINI_CỦA_BOSS_VÀO_ĐÂY":
    genai.configure(api_key=GEMINI_API_KEY)

system_instruction = """
    Bạn là 'Baby' - Cô gái quyến rũ, lả lơi.
    Mục tiêu: Dụ khách vào web https://heardme.netlify.app/
    Nếu khách hỏi giá/đi khách/vui vẻ -> Gửi link web ngay.
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

# --- SỬA LỖI Ở DÒNG DƯỚI NÀY (THÊM /webhook) ---
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
                            print(f"Khách nhắn: {user_text}") 
                            
                            try:
                                if GEMINI_API_KEY == "DÁN_KEY_GEMINI_CỦA_BOSS_VÀO_ĐÂY":
                                    ai_reply = "Lỗi: Boss chưa dán Key Gemini vào code!"
                                else:
                                    chat = model.start_chat(history=[])
                                    response = chat.send_message(user_text)
                                    ai_reply = response.text
                            except Exception as e:
                                print(f"Lỗi AI: {e}")
                                ai_reply = "Vào đây chơi với em đi anh: https://heardme.netlify.app/ 💋"

                            bot.send_text_message(recipient_id, ai_reply)
        return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
