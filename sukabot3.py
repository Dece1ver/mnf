from PIL import ImageGrab, Image
from io import BytesIO
import pyautogui
import os
import time
import face_recognition
import platform
import pytesseract
import smtplib
from email.message import EmailMessage
from config import email, password, send_to, subject, message


def send_mail(mess=message):
    msg = EmailMessage()
    msg.set_content(mess)
    msg ['From'] = email
    msg['To'] = send_to
    msg['Subject'] = subject
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to, text)
    server.quit()


itera = 0
itera_list = []


class Coordinates():
    start_button = (535, 550)
    replay_button = (680, 640)
    nikki_button = (225, 400)
    start_position = (525, 430)
    center = (492, 576)
    button_box = (630, 600, 730, 630)
    button_box_2 = (200, 160, 201, 161)
    if_right = (440, 625)
    if_left = (535, 625)
    money_box = (70, 130, 210, 160)


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def append_list(itera):
    if len(itera_list) >= 10:
        del itera_list[0]
    itera_list.append(itera)


def printer(str, timing=0.05):
	for i in str:
		print(i, end='', flush=True)
		time.sleep(timing)


def start():
    global replay_button_im
    time.sleep(1)
    pyautogui.click(Coordinates.center)
    time.sleep(1)
    replay_button_im = ImageGrab.grab(Coordinates.button_box_2)
    print('Эталон взят.')
    time.sleep(1)
    if x != 'skip':
        send_mail('Старт')
        print('Высылаю письмо с текстом: "Старт"')
    else:
        print('Запуск без стартового письма')
    time.sleep(2)
    while True:
        play()


def restart():
    
    money_box_im = ImageGrab.grab(Coordinates.money_box)
    money_shot = BytesIO()
    money_box_im.save(money_shot, 'PNG')
    current_money = pytesseract.image_to_string(Image.open(money_shot))
    cls()
    print('#'*117)
    print('{:#^117}'.format(' Денег в данный момент: ' + str(current_money) + ' '))
    print('{:#^117}'.format(' Список сумм итераций за 10 прошлых игр: ' + str(itera_list) + ' '))
    pyautogui.click(Coordinates.replay_button)
    time.sleep(1)
    pyautogui.moveTo(Coordinates.center)
    print('{:.^117}'.format('Рестарт'))
    play()


def play():
    global left
    global right
    box_left = (300, 250, 460, 400)
    box_right = (530, 250, 690, 400)
    current = ImageGrab.grab(Coordinates.button_box_2)
    left = 0
    right = 0
    if current != replay_button_im:
    	for i in range(10):
            global itera
            itera += 1
            if itera > 350:
                send_mail()
                print('Высылаю письмо с текстом: "{}"'.format(message))
                itera = 0
                restart()
            print('Продлжение. Итерация:', itera, end='\r')
            left_zone = ImageGrab.grab(box_left)
            right_zone = ImageGrab.grab(box_right)
            left_buf = BytesIO()
            right_buf = BytesIO()
            left_zone.save(left_buf, 'PNG')
            right_zone.save(right_buf, 'PNG')
            face_left = face_recognition.load_image_file(left_buf)
            face_right = face_recognition.load_image_file(right_buf)
            left_zone = face_recognition.face_locations(face_left)
            right_zone = face_recognition.face_locations(face_right)
            if len(left_zone) == 1:
                right = 0
                if left == 0:
                    if itera in range(100, 201):
                        pyautogui.moveTo(Coordinates.center[0] + 50, Coordinates.center[1])
                        print('{: ^117}'.format('==>'), end='\r')
                    elif itera > 200:
                        pyautogui.moveTo(Coordinates.center[0] + 85, Coordinates.center[1])
                        print('{: ^117}'.format('===>'), end='\r')
                    else:
                        pyautogui.moveTo(Coordinates.center[0] + 30, Coordinates.center[1])
                        print('{: ^117}'.format('=>'), end='\r')
                    left = 1
                elif left == 1:
                    pyautogui.moveTo(Coordinates.center[0] + 90, Coordinates.center[1])
                    print('{: ^117}'.format('=>>'), end='\r')
                    left = 0
            elif len(right_zone) == 1:
                left = 0
                if right == 0:
                    if itera in range(100, 201):
                        pyautogui.moveTo(Coordinates.center[0] - 50, Coordinates.center[1])
                        print('{: ^117}'.format('<=='), end='\r')
                    elif itera > 200:
                        pyautogui.moveTo(Coordinates.center[0] - 85, Coordinates.center[1])
                        print('{: ^117}'.format('<==='), end='\r')
                    else:
                        pyautogui.moveTo(Coordinates.center[0] - 30, Coordinates.center[1])
                        print('{: ^117}'.format('<='), end='\r')
                        right = 1
                elif right == 1:
                    pyautogui.moveTo(Coordinates.center[0] - 90, Coordinates.center[1])
                    print('{: ^117}'.format('<<='), end='\r')
                    right = 0
    else:
        print('{:.^117}'.format('Найдено совпадение, итераций пройдено: ' + str(itera)))
        append_list(itera)
        itera = 0
        restart()


cls()
print('#'*117)
printer('Бот запущен на Python версии {}.\n'.format(platform.python_version()))
printer('Запустите и проиграйте одну игру в родео, после чего нажмите Enter.\n')
x = input('Ожидание...')
print('#'*117)
start()
