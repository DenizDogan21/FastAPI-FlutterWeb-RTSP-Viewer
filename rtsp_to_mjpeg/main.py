# backend/main.py

import time
from fastapi import FastAPI, Response
import cv2
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# ==== Logging ====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI()
logging.info("🚀 FastAPI server initializing...")

# ==== CORS (for Flutter Web) ====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için uygundur. Prod'da değiştir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== RTSP Kamera Bağlantısı ====
# RTSP → FFmpeg → MediaMTX üzerinden gelen stream (örnek: rtsp://localhost:8554/mystream)
rtsp_url = "rtsp://localhost:8554/mystream"
logging.info(f"🎥 Connecting to RTSP stream: {rtsp_url}")
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    logging.error("❌ Kamera bağlantısı başarısız!")
else:
    logging.info("✅ Kamera bağlantısı başarılı.")

# ==== Kare Üretici ====
def generate_frames():
    cap = cv2.VideoCapture(rtsp_url)
    while True:
        success, frame = cap.read()
        if not success:
            logging.warning("⚠️ Frame alınamadı, RTSP kopmuş olabilir.")
            time.sleep(0.1)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# ==== MJPEG Akışı ====
@app.get("/video_feed")
def video_feed():
    logging.info("📡 Yeni MJPEG video isteği alındı.")
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

# ==== Ana başlatma ====
if __name__ == "__main__":
    logging.info("🚀 Sunucu başlatılıyor: http://0.0.0.0:5000")
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
