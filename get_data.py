import os
from cvzone.HandTrackingModule import HandDetector
import cv2
import copy
detector = HandDetector(maxHands=1)
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q",
          "R", "S", "T", "U", "V", "W", "X", "Y", "Nothing"]

dataset_size = 800
cap = cv2.VideoCapture(0)
frame_width = 1024
frame_height = 768
cap.set(3, frame_width)
cap.set(4, frame_height)
WIDTH = cap.get(3)
HEIGHT = cap.get(4)
for j in range(len(labels)):
    if not os.path.exists(os.path.join(DATA_DIR, str(labels[j]))):
        os.makedirs(os.path.join(DATA_DIR, str(labels[j])))

    print('Collecting data for class {}'.format(labels[j]))

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        cv2.putText(frame, f'Ready write {labels[j]}? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 1
    while counter <= dataset_size:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hands = detector.findHands(frame, draw=False)
        check = True
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            if x+w >= WIDTH or y+h >= HEIGHT or x < 1 or y < 1:
                check = False
            if check:
                frame2 = copy.copy(frame)
                cv2.putText(frame, 'Number Image {} :)'.format(counter), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                            cv2.LINE_AA)
                cv2.imwrite(os.path.join(DATA_DIR, str(
                    labels[j]), '{}_{}.jpg'.format(counter, labels[j])), frame2)
                counter += 1
            else:
                cv2.putText(frame, 'De ca ban tay vao trong ảnh :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                            cv2.LINE_AA)
        else:
            cv2.putText(frame, 'De tay vao trong anh :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                        cv2.LINE_AA)
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
cap.release()
cv2.destroyAllWindows()
