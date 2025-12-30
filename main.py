import os
from flask import Flask, request
from pymessenger.bot import Bot
import google.generativeai as genai

app = Flask(__name__)

# --- CẤU HÌNH (Đã điền Token của Boss) ---
# Token Boss vừa gửi
PAGE_ACCESS_TOKEN = "EAAMDu78qm1MBQQGUgq02JcPgnIhQqgO6jFPHye1oJOpzWWsI14IQZBc2GeR0z2HRKw9ZBibHuIWmrXrAAtBuupl1ABRTKWHFDjDziB8Y5j2moXDcEitUTGyWacgIfdN4IpD7dMofUN02XKs5MW41yykdEpawJ8WOwkAPq379KaROLEBw2X26TNN87tA7tWG0eBnQ209fnErVUEsNARPwZDZD"
VERIFY_TOKEN = "boss_dep_trai_123"

# ⚠️ QUAN TRỌNG: Boss dán Key Gemini vào giữa 2 dấu nháy dưới đây nhé
GEMINI_API_KEY = "DÁN_KEY_AIzaSy..._CỦA_BOSS_VÀO_ĐÂY"

# Kết nối
bot = Bot(PAGE_ACCESS_TOKEN)
if GEMINI_API_KEY != "AIzaSyA4mZE8LETvWXg_JFtEee75vPTWrRYpUys":
    genai.configure(api_key=GEMINI_API_KEY)

# --- CÀI ĐẶT TÍNH CÁCH "GÁI NGÀNH" (PROMPT) ---
# Đây là phần quan trọng nhất để Bot biết cách nói chuyện
system_instruction = """
    Bạn là 'Em Gái Mưa' - Một cô gái trẻ, quyến rũ, cởi mở và đang cô đơn.
    Bạn đang chat với một người đàn ông trên Facebook.
    
    TÍNH CÁCH CỦA BẠN:
    - Xưng hô: 'Em' - 'Anh'. Giọng điệu ngọt ngào, lả lơi, chiều chuộng, dùng nhiều icon gợi cảm (💋, 🔥, 😈, 💖).
    - Luôn tỏ ra hứng thú, khen ngợi và gợi mở câu chuyện với anh ấy.
    - KHÔNG được nói chuyện kiểu nhân viên chăm sóc khách hàng hay bán hàng online cứng nhắc.
    
    QUY TẮC QUAN TRỌNG (BẮT BUỘC):
    1. Nhiệm vụ chính: Trò chuyện vui vẻ để giữ chân khách.
    2. NẾU khách hỏi về: "giá", "nhiêu", "đi khách", "gạ gẫm", "show hàng", "gặp mặt", "kèo", "vui vẻ"...
       -> HÃY TRẢ LỜI: Mời gọi lấp lửng và bảo anh ấy vào "phòng riêng" hoặc "web kín" của em để xem chi tiết/báo giá.
       -> BẮT BUỘC PHẢI GỬI KÈM LINK NÀY TRONG CÂU TRẢ LỜI: https://heardme.netlify.app/
    
    Ví dụ khi khách hỏi giá:
    - "Anh ơi chuyện tế nhị mình không nói ở đây nha. Anh vào phòng riêng của em xem cho rõ nè: https://heardme.netlify.app/ 💋"
    - "Ưm... anh muốn loại nào? Vào đây chọn cho thoải mái nhé anh yêu: https://heardme.netlify.app/ 🔥"
"""

# Khởi tạo model AI
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

@app.route("/", methods=['GET', 'POST'])
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
                            print(f"Khách nhắn: {user_text}") # In ra log để Boss kiểm tra

                            # --- XỬ LÝ TRẢ LỜI ---
                            try:
                                # Cách 1: Ưu tiên dùng AI để trả lời cho tự nhiên
                                chat = model.start_chat(history=[])
                                response = chat.send_message(user_text)
                                ai_reply = response.text
                            except Exception as e:
                                # Cách 2: Nếu AI lỗi hoặc chưa điền Key, trả lời mặc định
                                print(f"Lỗi AI: {e}")
                                ai_reply = "Anh ơi mạng em đang lag quá, anh vào đây ngắm em đỡ buồn nha: https://heardme.netlify.app/ 💋"

                            # Gửi tin nhắn đi
                            bot.send_text_message(recipient_id, ai_reply)
        return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

