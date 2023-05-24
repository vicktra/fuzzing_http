import requests 
import threading #mô-đun chạy đa luồng
import argparse #mô-đun để phân tích đối số dòng lệnh

parser = argparse.ArgumentParser() #defines the parser

#Các đối số
parser.add_argument("-u", help="target url", dest='target')
parser.add_argument("--path", help="custom path prefix", dest='prefix')
parser.add_argument("--type", help="set the type i.e. html, asp, php", dest='type')
parser.add_argument("--fast", help="uses multithreading", dest='fast', action="store_true")
args = parser.parse_args() #đối số để được phân tích cú pháp

target = args.target #Nhận tarfet từ đối số

#Fancy banner :p
print ('''______   ______ _______ _______ _______ _     _ _______  ______
|_____] |_____/ |______ |_____| |       |_____| |______ |_____/
|_____] |    \_ |______ |     | |_____  |     | |______ |    \_
                          ''')

print ('\033[1;31m--------------------------------------------------------------------------\033[1;m\n')

try:
    target = target.replace('https://', '') #xóa chuỗi https://
except:
    print ('\033[1;31m[-]\033[1;m -u argument is not supplied. Enter python breacher -h for help')
    quit()

target = target.replace('http://', '') #xóa chuỗi http:// từ url
target = target.replace('/', '') #xóa / cuối url
target = 'http://' + target #thêm http:// đảm bảo có url hợp lệ
if args.prefix != None:
    target = target + args.prefix
try:
    r = requests.get(target + '/robots.txt') #gửi Requests đến example.com/robots.txt(web mục tiêu)
    if '<html>' in r.text:
        print ('  \033[1;31m[-]\033[1;m Robots.txt not found\n')
    else: 
        print ('  \033[1;32m[+]\033[0m Robots.txt found. Check for any interesting entry\n')
        print (r.text)
except: 
    print ('  \033[1;31m[-]\033[1;m Robots.txt not found\n')
print ('\033[1;31m--------------------------------------------------------------------------\033[1;m\n')

def scan(links):
    for link in links: #tìm nạp một liên kết từ danh sách liên kết
        link = target + link 
        r = requests.get(link) #Requests tới url
        http = r.status_code #phản hồi từ server
        if http == 200: # in ra dấu [+]
            print ('  \033[1;32m[+]\033[0m Admin panel found: %s'% link)
        elif http == 404:
            print ('  \033[1;31m[-]\033[1;m %s'% link)
        elif http == 302: #in ra dấu [+]
            print ('  \033[1;32m[+]\033[0m Potential EAR vulnerability found : ' + link)
        else:
            print ('  \033[1;31m[-]\033[1;m %s'% link)
paths = [] #list of paths
def get_paths(type):
    try:
        with open('paths.txt','r') as wordlist: #mở đường dẫn.txt và lấy các liên kết theo loại đối số
            for path in wordlist: 
                path = str(path.replace("\n",""))
                try:
                    if 'asp' in type:
                        if 'html' in path or 'php' in path:
                            pass
                        else:
                            paths.append(path)
                    if 'php' in type:
                        if 'asp' in path or 'html' in path:
                            pass
                        else:
                            paths.append(path)
                    if 'html' in type:
                        if 'asp' in path or 'php' in path:
                            pass
                        else:
                            paths.append(path)
                except:
                    paths.append(path)
    except IOError:
        print ('\033[1;31m[-]\033[1;m Wordlist not found!')
        quit()

if args.fast == True: #nếu người dùng đã cung cấp đối số --fast
    type = args.type #lấy đầu vào từ đối số --type
    get_paths(type) #yêu cầu trình lấy liên kết, lấy các liên kết theo đầu vào của người dùng như php, html, asp
    paths1 = paths[:len(paths)/2] #Danh sách đường dẫn/liên kết 
    paths2 = paths[len(paths)/2:] #chia thành hai danh sách
    def part1():
        links = paths1 #là phần đầu tiên của danh sách
        scan(links) #calls the scanner
    def part2():
        links = paths2 # là phần thứ 2 của danh sách
        scan(links) #calls the scanner
    t1 = threading.Thread(target=part1) #tạo 1 luồng cho part1
    t2 = threading.Thread(target=part2) #tạo 1 luồng cho part2
    t1.start() #starts luồng 1
    t2.start() #starts luồng 2
    t1.join() 
    t2.join()
else: 
    type = args.type
    get_paths(type)
    links = paths
    scan(links)