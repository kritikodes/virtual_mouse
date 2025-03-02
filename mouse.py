import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

click_state = False
scroll_state = False
scroll_start_y = None

cap = cv2.VideoCapture(0)

while True:
    
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    output = hands.process(rgb_frame)
    hands_landmarks = output.multi_hand_landmarks

    if hands_landmarks:
        for landmarks in hands_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            
            index_finger = landmarks.landmark[8]
            middle_finger = landmarks.landmark[12]
            thumb_finger = landmarks.landmark[4]
            
            index_x = int(index_finger.x * frame_width)
            index_y = int(index_finger.y * frame_height)
            index_screen_x = int(index_finger.x * screen_width)
            index_screen_y = int(index_finger.y * screen_height)

            middle_x = int(middle_finger.x * frame_width)
            middle_y = int(middle_finger.y * frame_height)
            
            thumb_x = int(thumb_finger.x * frame_width)
            thumb_y = int(thumb_finger.y * frame_height)
            
            cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)  
            cv2.circle(frame, (middle_x, middle_y), 10, (0, 255, 0), -1)  
            cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), -1) 

            pyautogui.moveTo(index_screen_x, index_screen_y)
            
            if abs(index_y - thumb_y) < 30 and abs(index_x - thumb_x) < 30:
                if not click_state:
                    pyautogui.click()
                    click_state = True
            else:
                click_state = False

            if abs(index_y - middle_y) < 30:
                if not scroll_state:
                    scroll_start_y = index_y
                    scroll_state = True
                else:
                    scroll_delta = index_y - scroll_start_y
                    pyautogui.scroll(-scroll_delta * 2)  
                    scroll_start_y = index_y
            else:
                scroll_state = False

    cv2.imshow("Virtual Mouse", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
