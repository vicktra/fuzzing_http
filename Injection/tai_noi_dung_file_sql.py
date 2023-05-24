import requests
from bs4 import BeautifulSoup

url = "http://testphp.vulnweb.com/admin/"
response = requests.get(url)

# Kiểm tra mã trạng thái của yêu cầu
if response.status_code == 200:
    # Lấy nội dung HTML của trang web
    content = response.text

    # Sử dụng BeautifulSoup để phân tích cú pháp HTML
    soup = BeautifulSoup(content, "html.parser")

    # Tìm tất cả các thẻ <a href> trong trang web
    a_tags = soup.find_all("a")

    # In ra các đường dẫn trong các thẻ <a href>
    for a_tag in a_tags:
        print(a_tag["href"])
else:
    print("Yêu cầu không thành công. Mã trạng thái:", response.status_code)
    #kiem tra thấy có file crate.sql tải file đó về
url = "http://testphp.vulnweb.com/admin/create.sql"
response = requests.get(url)

# Kiểm tra xem yêu cầu tải xuống đã thành công hay chưa
if response.status_code == 200:
    # Lưu file tải xuống với tên create.sql
    with open("create.sql", "wb") as file:
        file.write(response.content)
    print("Tải xuống thành công!")
else:
    print("Lỗi khi tải xuống file.")

# Đọc nội dung của file create.sql đã tải xuống
with open("create.sql", "r") as file:
    content = file.read()

# In nội dung của file ra màn hình
print(content)