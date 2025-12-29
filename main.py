from flask import Flask, request

app = Flask(__name__)

# 1. Xác minh với Facebook (Chỉ làm đúng 1 lần đầu tiên)
@app.route('/webhook', methods=['GET'])
def verify():
    # Facebook gửi mã verify, mình trả lại đúng mã đó là xong
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        return request.args.get("hub.challenge")
    return "Lỗi xác minh", 403

# 2. Nhận tin nhắn (Chạy tự động vĩnh viễn)
@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.json # Dữ liệu tin nhắn khách gửi đến nằm ở đây
    print("Có tin nhắn mới:", data)
    
    # [CHỖ NÀY BOSS GỌI GEMINI XỬ LÝ RỒI TRẢ LỜI LẠI]
    
    return "Đã nhận", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)