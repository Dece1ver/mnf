import time
import os
import cv2
import mss
import numpy
import pyautogui
import face_recognition

pyautogui.FAILSAFE = False
input('Расположить все как надо и Enter')
with mss.mss() as sct:
    # Part of the screen to capture
    restart_screen = {"top": 115, "left": 65, "width": 5, "height": 5}
    monitor = {"top": 115, "left": 197, "width": 288, "height": 145}
    monitor_center = int(monitor['width']/2)
    restart_img = numpy.array(sct.grab(restart_screen))
    restart_img = cv2.cvtColor(restart_img, cv2.COLOR_BGR2GRAY)
    print('Эталон взят')
    time.sleep(1)
    start_time = time.time()
    times_list = []

    while "Screen capturing":
        os.system('cls')
        current_scr = numpy.array(sct.grab(restart_screen))
        current_scr = cv2.cvtColor(current_scr, cv2.COLOR_BGR2GRAY)
        if (time.time()-start_time) > 52:
            print('\nКончаем.', end='')
            while not numpy.array_equal(current_scr, restart_img):
                print('.', end='')
                current_scr = numpy.array(sct.grab(restart_screen))
                current_scr = cv2.cvtColor(current_scr, cv2.COLOR_BGR2GRAY)
                time.sleep(1)           
        if numpy.array_equal(current_scr, restart_img):
            pyautogui.click(425,390)
            pyautogui.click(425,400)
            pyautogui.click(425,415)
            # pyautogui.click(425,435)
            pyautogui.moveTo(400, monitor_center)
            time.sleep(2)
            times_list.append(round(time.time()-start_time-9, 1))
            if len(times_list) > 6:
                del times_list[0]
            start_time = time.time()        
        for i in range(50):
            last_time = time.time()
            img = numpy.array(sct.grab(monitor))
            gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.line(gimg, (monitor_center, 0), (monitor_center, monitor['height']), (255,255,255), 2)
            face = face_recognition.face_locations(gimg)
            for (top, right, bottom, left) in face:
                face_center  = (right-int((right-left)/2), top)
                cv2.rectangle(gimg, (left, bottom), (right, top), (255,0,0), 2)               
                cv2.line(gimg, face_center, (face_center[0], face_center[1]+(bottom-top)), (0,255,0), 2)
                if face_center[0] < monitor_center:
                    pyautogui.move(monitor_center-face_center[0], 0)
                elif face_center[0] > monitor_center:
                    pyautogui.move(monitor_center-face_center[0], 0)
            cv2.imshow("OpenCV/Numpy normal", gimg)
            try:
                print(f"FPS: [{1 / (time.time() - last_time):>-05.2f}] Time: [{time.time()-start_time-1.5:>-05.2f}] Last games: {times_list}", end = '\r')
            except ZeroDivisionError as e:
                pass
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break