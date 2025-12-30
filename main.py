from flask import Flask, request
import requests

app = Flask(__name__)

# ================= CẤU HÌNH ĐÃ NHẬP SẴN =================
# Token của Page "Chat Girl" Boss đã gửi
PAGE_ACCESS_TOKEN = "EAAMDu78qm1MBQc887o6SLuauIy2zWzR787Ac6u8Ty4dj8xZC2PEZBriuoU9djlPtnJaE4yOpXdb5LB4oN8lT1HJqTa5nrJPaZCU1Y0ZAMHHjYJzFuCVozkTRBCzIzflYaJGYXQk1vGQ2J91dY7pYBLIuLagYBqoZCnZBKIDF6ZCvsbAZBs7m7YeevQMrQjZCCyMMy3cYUYqkIeJriDcUv9b8q0gZDZD"

# Mã verify
VERIFY_TOKEN = "boss_dep_trai_123"
# ========================================================

@app.route('/', methods=['GET'])
def home():
    return "Bot Chat Girl đang chạy!", 200

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
    return "Sai mã verify", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry.get("messaging", []):
                if "message" in messaging_event:
                    sender_id = messaging_event["sender"]["id"]
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]
                        
                        # LOGIC TRẢ LỜI ĐƠN GIẢN (TEST)
                        tra_loi_khach(sender_id, "Em nhận được tin của anh rồi: " + message_text)
                        
    return "OK", 200

def tra_loi_khach(nguoi_nhan_id, noi_dung):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": nguoi_nhan_id},
        "message": {"text": noi_dung}
    }
    requests.post("https://graph.facebook.com/v21.0/me/messages", params=params, headers=headers, json=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

