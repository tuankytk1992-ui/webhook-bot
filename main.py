import os
from flask import Flask, request
from pymessenger.bot import Bot
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)

# --- CẤU HÌNH FACEBOOK ---
PAGE_ACCESS_TOKEN = "EAAMDu78qm1MBQQGUgq02JcPgnIhQqgO6jFPHye1oJOpzWWsI14IQZBc2GeR0z2HRKw9ZBibHuIWmrXrAAtBuupl1ABRTKWHFDjDziB8Y5j2moXDcEitUTGyWacgIfdN4IpD7dMofUN02XKs5MW41yykdEpawJ8WOwkAPq379KaROLEBw2X26TNN87tA7tWG0eBnQ209fnErVUEsNARPwZDZD"
VERIFY_TOKEN = "boss_dep_trai_123"

# --- LẤY KEY TỪ KÉT SẮT RENDER (AN TOÀN TUYỆT ĐỐI) ---
api_key = os.environ.get("GEMINI_API_KEY")

bot = Bot(PAGE_ACCESS_TOKEN)

# --- CẤU HÌNH TÍNH CÁCH ---
system_instruction = """
    Bạn là 'Baby' - Cô gái cực kỳ quyến rũ, táo bạo và chiều khách.
    
    LUẬT CHƠI:
    - Xưng hô: 'Em' - 'Anh'. Dùng nhiều icon gợi tình (💋, 🔥, 🤤).
    - MỤC TIÊU: Dụ khách bấm vào link: https://heardme.netlify.app/
    
    KỊCH BẢN:
    - Khách: "Ngon không?", "Show hàng", "Đi khách không?", "Giá sao?"
    - Bot: "Ngon hay không anh vào xem thử là biết liền à, nước nôi đầy đủ: https://heardme.netlify.app/ 🤤"
    - Khách chat bình thường -> Trả lời lả lơi, rủ rê.
"""

# Tháo xích an toàn (18+)
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# Cấu hình AI
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction, safety_settings=safety_settings)

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
                            
                            try:
                                if not api_key:
                                    ai_reply = "Lỗi: Boss chưa nhập Key vào Environment trên Render!"
                                else:
                                    chat = model.start_chat(history=[])
                                    response = chat.send_message(user_text)
                                    ai_reply = response.text
                            except Exception as e:
                                print(f"Lỗi: {e}")
                                ai_reply = "Anh ơi mạng lag quá, vào đây chơi với em đi: https://heardme.netlify.app/ 💋"

                            bot.send_text_message(recipient_id, ai_reply)
        return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
