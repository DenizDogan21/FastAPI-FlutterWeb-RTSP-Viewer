# MJPEG Stream Viewer

A Flutter web application with a FastAPI backend to display MJPEG streams from RTSP sources, such as security cameras or IoT devices. The Flutter frontend renders the MJPEG stream using a browser-native `<img>` element, while the FastAPI backend converts an RTSP stream into MJPEG format for web consumption.

## Features
- **Cross-Platform Frontend**: Built with Flutter, optimized for web, with potential for mobile support.
- **RTSP to MJPEG Conversion**: FastAPI backend processes RTSP streams using OpenCV and serves them as MJPEG.
- **Simple Setup**: Easy-to-configure backend and frontend in a single repository.
- **Error Handling**: Graceful handling of stream failures with customizable error UI.

## Prerequisites
- **Flutter**: Version 3.0.0 or higher (for web support)
- **Python**: Version 3.8 or higher
- **FFmpeg**: Required for RTSP stream processing
- **MediaMTX**: Used to proxy RTSP streams (e.g., `rtsp://localhost:8554/mystream`)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mjpeg-stream-viewer.git
cd mjpeg-stream-viewer
```

### 2. Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn opencv-python
   ```
4. Ensure MediaMTX is running and your RTSP stream is available at `rtsp://localhost:8554/mystream`.
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000
   ```

### 3. Frontend Setup
1. Navigate to the `flutter_app` directory:
   ```bash
   cd flutter_app
   ```
2. Install Flutter dependencies:
   ```bash
   flutter pub get
   ```
3. Run the Flutter web app:
   ```bash
   flutter run -d chrome
   ```

### 4. Verify the Stream
- Open your browser and navigate to `http://localhost:5000/video_feed` to confirm the MJPEG stream is accessible.
- The Flutter app should display the stream at `http://localhost:5000/video_feed`.

## Project Structure
```
mjpeg-stream-viewer/
├── backend/
│   ├── main.py             # FastAPI backend to convert RTSP to MJPEG
│   └── requirements.txt    # Python dependencies
├── flutter_app/
│   ├── lib/
│   │   └── main.dart       # Flutter frontend to display MJPEG stream
│   ├── web/
│   │   └── index.html      # Web entry point
│   └── pubspec.yaml        # Flutter dependencies
└── README.md               # Project documentation
```

## Usage

### Backend
The `main.py` file in the `backend` directory sets up a FastAPI server that:
- Connects to an RTSP stream (default: `rtsp://localhost:8554/mystream`).
- Converts the stream to MJPEG using OpenCV.
- Serves the MJPEG stream at `http://localhost:5000/video_feed`.

To change the RTSP source, update the `rtsp_url` in `main.py`:
```python
rtsp_url = "rtsp://your-camera-ip:8554/stream"
```

### Frontend
The `main.dart` file in `flutter_app/lib` uses Flutter’s `HtmlElementView` to display the MJPEG stream in a web browser. The stream URL is set to `http://localhost:5000/video_feed` by default. To change it:
```dart
final String streamUrl = 'http://your-backend-ip:5000/video_feed';
```

### Running in Production
1. **Backend**:
   - Deploy the FastAPI server on a production server (e.g., AWS, Heroku).
   - Update CORS settings in `main.py` for your domain:
     ```python
     app.add_middleware(
         CORSMiddleware,
         allow_origins=["https://your-app-domain.com"],
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )
     ```
   - Use HTTPS for secure communication.
2. **Frontend**:
   - Build the Flutter web app:
     ```bash
     flutter build web --web-renderer html --release
     ```
   - Deploy the `build/web` folder to a static hosting service (e.g., Firebase, Netlify).
   - Update the `streamUrl` in `main.dart` to match your backend’s production URL.

## Dependencies
- **Backend**:
  - FastAPI
  - Uvicorn
  - OpenCV-Python
- **Frontend**:
  - Flutter
  - `html` package (`^0.15.0`)

## Troubleshooting
- **Stream Not Loading**:
  - Verify the RTSP stream in VLC: `rtsp://localhost:8554/mystream`.
  - Check the backend logs for errors (`uvicorn main:app`).
  - Ensure CORS is correctly configured.
- **Flutter Errors**:
  - Confirm the `html` package is installed (`flutter pub get`).
  - Check browser console (F12) for network or CORS issues.
- **Performance**:
  - Use the HTML renderer (`--web-renderer html`) for smaller build size.
  - Optimize RTSP stream resolution to reduce bandwidth.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue on GitHub.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, contact [your-email@example.com](mailto:your-email@example.com) or open an issue on GitHub.