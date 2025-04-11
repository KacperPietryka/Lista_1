from collections import deque
import os
import shutil
import datetime
import webbrowser
from pypdf import PdfWriter
import qrcode
import cv2
import requests

def check_brackets(input):
    stack = deque()
    for i in input:
        if i == '[' or i == '(' or i == '{' or i == '<':
            stack.append(i)
        elif i == ')' or i == '}' or i == ']' or i == '>':
            if len(stack) == 0:
                return False
            value = stack.pop()
            if (i == ')' and value != '(') or (i == '}' and value != '{') or (i == ']' and value != '[') or (i == '>' and value != '<'):
                return False
        else: 
            continue
    return len(stack) == 0

def copy_files(list_of_files, list_of_extensions, where_save = r'C:\Users\Kacper\backup'):
    date = str(datetime.date.today())
    where_save = os.path.join(where_save, date)
    os.makedirs(where_save, exist_ok=True)
    for directory in list_of_files: # going through the list of user given directories
        for root, _, files in os.walk(directory):
            for file in files:
                for extension in list_of_extensions: # searching for a particular extension
                    length = len(extension)
                    if file[-length:] == extension:
                        location = os.path.join(root, file)
                        shutil.copy(location, where_save)

def merge_PDF(catalog_with_PDFs, output = r'C:\Users\Kacper\new_file.pdf'):
    pdfWriter = PdfWriter()
    print(catalog_with_PDFs)
    for root, dirs, files in os.walk(catalog_with_PDFs):
        for file in files:
            location = os.path.join(root, file)
            pdfWriter.append(location)
            if file[-4:] == '.pdf':
                with open(output, 'wb') as f:
                    pdfWriter.write(f)

def change_format(file, original_type):
    with open(file, 'rb') as f:
        file_string = f.read().decode('utf-8')
        if original_type == 'windows':
            file_string = file_string.replace('\r', '')
        elif original_type == 'unix' or original_type == 'macos':
            file_string = file_string.replace('\n', '\r\n')
        return repr(file_string)

def create_QRcode(data, filename = 'qr_code.jpg'):
    image = qrcode.make(data)
    image.save(filename)
    return image

def read_QRcode(image):
    image = cv2.imread(image)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    cv2.imshow(f"QR Code of: {data}", image)
    cv2.waitKey(0) # wait until the file is closed
    cv2.destroyAllWindows()
    return data

def Wiki_article():
    url = 'https://en.wikipedia.org/wiki/Special:Random'
    picked_article = False
    while picked_article == False:
        title = searching(url)
        print(f'Selected title: {title}')
        key = input('If you like the topic, type y!')
        if key == 'y':
            webbrowser.open(url)
            picked_article = True

def searching(url):
    response = requests.get(url)
    if response.status_code != 200:
        return f'Error {response}! Can not open a site'
    search = 'title'
    title = ''
    index = 0
    for i in response.text:
        if index != len(search):
            if search[index] == i:
                index += 1
            else:
                index = 0
        else:
            if i != '<':
                title += i
            else:
                break
    return title


Wiki_article()
#read_QRcode('qr_code.jpg')
create_QRcode('https://en.wikipedia.org/wiki/Main_Page')
change_format('C:\\Users\\Kacper\\Downloads\\unix_example.txt', 'unix')
merge_PDF(r'D:\Python App\app\app\Media\pdfs')
copy_files([r'D:\Python App\app\app\Media', r'D:\Python App\ksiazka'], ['.jpg', '.png'])


input_ = "<html><head></head><body></body></html>"
X = check_brackets(input_)
if X:
    print('Brackets are balanced')
else:
    print('Brackets are not balanced')