import cv2
from ultralytics import YOLO
import time
import os
import json
import requests

# Load config from config.json
with open("config.json", "r") as f:
    config = json.load(f)

TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
CHAT_ID = config["CHAT_ID"]

# Settings
TARGET_CLASS = "person"
CONFIDENCE_THRESHOLD = 0.5

# Telegram message function
def send_telegram_message(text, photo_path=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}

    try:
        requests.post(url, data=data)

        if photo_path and os.path.exists(photo_path):
            url_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            with open(photo_path, "rb") as photo:
                requests.post(url_photo, data={"chat_id": CHAT_ID}, files={"photo": photo})
    except Exception as e:
        print("❌ Telegram error:", e)

# Load YOLO model
model = YOLO("yolov8n.pt")

# Create alerts folder
os.makedirs("alerts", exist_ok=True)

# Camera
cap = cv2.VideoCapture(0)

print(f"🔍 Looking for: {TARGET_CLASS}")

while True:
    success, frame = cap.read()
    if not success:
        break

    results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
    alert_triggered = False
    filename = None

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls = int(box.cls[0].item())
            class_name = model.names[cls]
            conf = box.conf[0].item()

            if class_name == TARGET_CLASS:
                alert_triggered = True
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                cv2.putText(frame, f"ALERT: {class_name} {conf:.2f}",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}",
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if alert_triggered:
        filename = f"alerts/alert_{int(time.time())}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Alert saved: {filename}")
        send_telegram_message("🚨 Person detected!", filename)

    cv2.imshow("AI Security Monitor", frame)

    if cv2.waitKey(1) == 27:  # 27 = ESC
        break


cap.release()
cv2.destroyAllWindows()
