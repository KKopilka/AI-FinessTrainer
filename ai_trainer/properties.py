import cv2
import time
from AudioCommSys import text_to_speech
import threading

def illustrate_exercise(example): 
    list_threads = []
    seconds = 4
    img = cv2.imread(example)
    img = cv2.resize(img, (980, 550))
    while seconds > 0:
        frame_copy = img.copy()
        speaker_thread = threading.Thread(
            target=text_to_speech, args=(str(int(seconds))), kwargs={}
            
        )
        speaker_thread.start()
        speaker_thread.join()
        # time.sleep(1)
        cv2.putText(
            frame_copy,
            "Exercise in: " + str(int(seconds)),
            (350, 50),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (0, 0, 255),
            5,
        )
        cv2.imshow("Video", frame_copy)
        cv2.waitKey(1000)
        seconds -= 1

def score_table(img, count):
    text = "Your score: " + str(count)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255) 

    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_width, text_height = text_size

    text_x = 10
    text_y = 50
    padding = 5
    background_x = text_x - padding
    background_y = text_y - text_height - padding
    background_width = text_width + 2 * padding
    background_height = text_height + 2 * padding

    cv2.rectangle(img, (5, 23), (5 + background_width, 23 + background_height), (30, 144, 255), -1, cv2.LINE_AA)
    cv2.putText(img, text, (10, 50), font, font_scale, font_color, font_thickness)

    return img