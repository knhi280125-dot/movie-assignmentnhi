from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

# Khởi tạo Flask với biến tên là app
app = Flask(__name__)

# Kết nối Firebase - Nhi nhớ file json phải nằm cùng thư mục nhé
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Lỗi kết nối Firebase: {e}")

@app.route("/")
def index():
    # Trang chủ dẫn đến link tìm kiếm
    return '<a href="/searchQ">[ 查詢即將上映電影 ]</a>'

@app.route("/searchQ", methods=["POST", "GET"])
def searchQ():
    if request.method == "POST":
        # Lấy tên phim từ ô nhập liệu
        MovieTitle = request.form.get("MovieTitle", "")
        info = ""
        
        # Truy vấn bảng 電影 (Nhi nhớ kiểm tra tên bảng trong Firebase nhé)
        collection_ref = db.collection("電影")
        docs = collection_ref.get()
        
        for doc in docs:
            movie_data = doc.to_dict()
            # Nếu để trống hoặc khớp tên phim thì hiện ra
            if MovieTitle == "" or MovieTitle in str(movie_data.get("title", "")):
                info += f"片名：{movie_data.get('title', '無')}<br>"
                info += f"影片介紹：{movie_data.get('hyperlink', '無')}<br>"
                info += f"片長：{movie_data.get('showLength', '未知')} 分鐘<br>"
                info += f"上映日期：{movie_data.get('showDate', '未知')}<br><br>"
        
        if info == "":
            return "抱歉，找不到相關電影資料。請 kiểm tra lại tên phim trong Firebase nhé!"
        return info
    else:
        # Hiển thị file input.html trong thư mục templates
        return render_template("input.html")

# Dòng này cực kỳ quan trọng để Vercel nhận diện được app
app = app
