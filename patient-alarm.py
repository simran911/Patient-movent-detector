import threading
import winsound
import cv2
import imutils
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send email
def send_email():
    from_addr = "simran11singh2004@gmail.com"  # Your email address
    to_addr = "somasingh08892@gmail.com"  # Recipient's email address
    password = "sim@tan911"  # Your email password

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Detection Found!"

    body = "Detection found in the camera feed. Please take necessary action."
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

_, start_frame = cap.read()
start_frame = cv2.resize(start_frame, (500, 375))  # Resize start_frame
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        winsound.Beep(2500, 1000)

while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (500, 375))  # Resize frame

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 300:
            alarm_counter += 1
            if alarm_counter > 20:
                if not alarm:
                    alarm = True
                    threading.Thread(target=beep_alarm).start()
                    threading.Thread(target=send_email).start()
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("CAM", threshold)
    else:
        cv2.imshow("CAM", frame)

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break
                
              
              
cap.release()
cv2.destroyAllWindows()
