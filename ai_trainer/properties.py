import cv2
import time
from AudioCommSys import text_to_speech
import threading

# class utilities:
# list_threads = []

# def __init__(self) -> None:
#     pass

def illustrate_exercise(example): 
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

def calculate_counter(per, count, dirr): 
    color = (255, 0, 255)
    # print("per: ", per)
    if per == 100:
        color = (0, 255, 0)
        if dirr == 0:
            # count += 0.5
            dirr = 1
    # полное выполнение упражнения
    if per == 0:
        color = (0, 255, 0)
        if dirr == 1:
            count += 1
            dirr = 0
    print(count)
    
#     color = (255, 0, 255)
    
#     if per >= 70:  # Условие для увеличения счетчика при выполнении упражнения (например, угол больше или равен 90 градусам)
#         color = (0, 255, 0)
#         if dirr == 0:
#             dirr = 1
#     elif per <= 10:  # Условие для увеличения счетчика при полном выполнении упражнения (например, угол меньше или равен 10 градусам)
#         color = (0, 255, 0)
#         if dirr == 1:
#             count += 1
#             dirr = 0
    return [count, dirr]
# # def calculate_counter(self, angle, count, dirr):
#     color = (255, 0, 255)
#     if angle == 100:
#         color = (0, 255, 0)
#         if dirr == 0:
#             dirr = 1
#     # полное выполнение упражнения
#     if angle == 0:
#         color = (0, 255, 0)
#         if dirr == 1:
#             count += 1
#             dirr = 0

#     return [count, dirr]


def score_table(img, count):
    # cv2.putText(frame, "Activity : " + exercise.replace("-", " "),
    #             (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2,
    #             cv2.LINE_AA)
    cv2.putText(img, "Your score : " + str(count), (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    return img
class DirectionCounter():
    enabled = True
    dirr = 0
    positive = 100
    negative = 0
    counter = 0

    def __init__(self, positive=100, negative=0):
        self.positive = positive
        self.negative = negative

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def count(self, per):
        if not self.enabled:
            return
        if per == self.positive:
            if self.dirr == 0:
                self.dirr = 1

        if per == self.negative:
            if self.dirr == 1:
                self.counter += 1
                self.dirr = 0

    def reset(self):
        self.dirr = 0
        self.counter = 0

    def get(self):
        return self.counter