import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
x1 = y1 = x2 = y2 = 0
previous_distance = 0

while True:
    data, image = cap.read()
    image = cv2.flip(image, 1)
    frame_height, frame_width, depth = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for index, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if index == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y

                if index == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y

        distance = (((x2-x1)**2 + (y2-y1)**2)**0.5)//4
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        control = previous_distance - distance
        previous_distance = distance
        if control < -15:
            pyautogui.press("volumeup", 5)
        elif control > 15:
            pyautogui.press("volumedown", 5)

    cv2.imshow('Hand Tracker', image)
    key = cv2.waitKey(10)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
