import cv2
import time
from AudioCommSys import text_to_speech
import threading

def illustrate_exercise(example): 
    list_threads = []
    seconds = 4
    img = cv2.imread(example)
    print(img.shape)
    img = cv2.resize(img, (980, 550))
    while seconds > 0:
        frame_copy = img.copy()
        # speaker_thread = threading.Thread(
        #     target=text_to_speech, args=(str(int(seconds))), kwargs={}
            
        # )
        
        # speaker_thread.start()
        # speaker_thread.join()
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
    cv2.putText(img, "Your score : " + str(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return img