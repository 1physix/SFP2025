import cv2
import mediapipe as mp
import pyautogui
import turtle as t
pyautogui.FAILSAFE = False
click = False
screen_w, screen_h = pyautogui.size() #gets the size of the screen of your device
camera = cv2.VideoCapture(0) #Telling cv2 that it has to record video

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True) #creates refined landmarks on the face, identifying different parts of the face
pyautogui.moveTo(screen_w/2, screen_h/2)

"""-----Turtle Stuff-----"""
window = t.Screen()
t.Screen().setup(screen_w, screen_h, 0, 0)
t.goto(0, 0)
t.speed(100)
t.shape("turtle")
t.color("blue")
t.pensize(5)

def move(x, y):
    t.goto(x, y)

window.onclick(move)
"""-----Turtle Stuff-----"""
select_click_eye = input("""What eye would you like to click with?
-> Left
-> Right
------>""")

while True:
#Because a video is a constantly moving image that generates frames constant,
#we have to put a permanant loop to read every frame

    _, frame = camera.read()
    frame = cv2.flip(frame,1 ) #since frame is mirrored, we flip it to "unmirror" it.
    coloured_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #making the video colourful

    output = face_mesh.process(coloured_frame) #just outputting the coloured frame

    facial_landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if facial_landmark_points:
        landmarks = facial_landmark_points[0].landmark #gives an x-y decimal porportion of the frame

        if select_click_eye.lower() == "left":
            click_eye = [landmarks[145], landmarks[159]]

        elif select_click_eye.lower() == "right":
            click_eye = [landmarks[374], landmarks[386]]
        else:
            print("Invalid option. Please run again.")

        cursor = [landmarks[4]]

        for mouse_move, landmark in enumerate(cursor):
            x = int(landmark.x * frame_w)  #creating a x coordinate with the x-porportion of the frame and the width to find the x-coordinate
            y = int(landmark.y * frame_h)  #creating a y  coordinate with the y-porportion of the frame and the height to find the y-coordinate
            cv2.circle(frame, (x,y), 10, (0,255,0)) #drawing a circle around the point with the corresponding x,y coordinates
            #print(x,y) #just printing the coordinates as text
            screen_x = (x / frame_w) * screen_w * 1.5
            screen_y = (y / frame_h) * screen_h * 1.7
            pyautogui.moveTo(screen_x, screen_y, 0.1)

        #^^The camera frame is smaller than the device screen, so we have to scale up the mouse movements by the ratio of the sizes^^#




        for landmark in click_eye:
            y = int(landmark.y * frame_h)
            x = int(landmark.x * frame_w)
            cv2.circle(frame, (x, y), 5, (0, 0, 255))
            eye_width = abs(landmarks[133].x - landmarks[362].x)  # Outer eye corners
            blink_threshold = eye_width * 0.2  # 20% of eye width

            if abs(click_eye[0].y - click_eye[1].y) < blink_threshold:
                print("Click")
                """If the distance between the eyelids is less that 0.003, we print the word click"""
                pyautogui.click()
                pyautogui.sleep(1)
                print(f"Y_DIFF {(click_eye[0].y - click_eye[1].y)}")
                print(f"X_DIFF {click_eye[0].x - click_eye[1].x}")

    window.update()
    cv2.imshow("Eye Tracking", frame)  # This makes the video actually show on the computer.


    cv2.waitKey(1) # in case we want to stop the video with a key press, this waits for a key press.

