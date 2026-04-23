@app.route("/searchQ", methods=["POST", "GET"])
def searchQ():
    if request.method == "POST":
        MovieTitle = request.form["MovieTitle"]
        info = ""
        collection_ref = db.collection("電影")
        # Lấy tất cả phim ra luôn
        docs = collection_ref.get() 
        
        for doc in docs:
            電影資料 = doc.to_dict()
            # Nếu để trống ô tìm kiếm hoặc nhập đúng tên thì đều hiện ra
            if MovieTitle == "" or MovieTitle in 電影資料.get("title", ""):
                info += "片名：" + str(電影資料.get("title", "無")) + "<br>"
                info += "影片介紹：" + str(電影資料.get("hyperlink", "無")) + "<br>"
                info += "片長：" + str(電影資料.get("showLength", "未知")) + " 分鐘<br>"
                info += "上映日期：" + str(電影資料.get("showDate", "未知")) + "<br><br>"
        
        return info if info != "" else "Firebase đang trống, Nhi hãy thêm phim vào bảng 電影 nhé!"
    else:
        return render_template("input.html")
