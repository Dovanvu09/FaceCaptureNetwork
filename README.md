
# FaceDataCollector

## 📖 Project Description
**FaceDataCollector** is a client-server system designed to capture and process facial data using a webcam. It facilitates the collection of labeled face data for biometric analysis and other applications.

The project consists of two main components:
- **Client**: Captures user video, extracts frames, and sends them to the server with associated metadata.
- **Server**: Validates, stores, and processes the received frames.

---

## 🌟 Features
### Client:
- Prompt user for a label (e.g., name) to associate with their face data.
- Configure video settings, including FPS, resolution, and frame size.
- Capture video with diverse facial expressions and angles.
- Extract frames from the video and send them in batches to the server.
- Receive feedback on frame quality (e.g., resolution, missing data).
- Option to request previously sent images from the server.

### Server:
- Manage user sessions with token-based authentication.
- Validate incoming frames for resolution, compression, and face detection.
- Provide feedback and request frame adjustments if required.
- Store valid frames in a database.
- Respond to client requests for stored frames.

---

## 📂 Project Structure
```
FaceDataCollector/
│
├── client/                # Client-side application
│   ├── capture.py         # Handles video capture and frame extraction
│   ├── uploader.py        # Sends frames to the server
│   ├── config.json        # Configuration for video settings
│   └── gui.py             # User interface for client
│
├── server/                # Server-side application
│   ├── app.py             # Main server application
│   ├── database.py        # Handles database operations
│   ├── frame_validator.py # Validates received frames
│   ├── api.py             # RESTful API endpoints
│   └── config.yaml        # Server configuration
│
├── tests/                 # Unit tests for client and server
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

---

## ⚙️ Installation
### Prerequisites
- Python 3.8 or higher
- Required libraries: OpenCV, Flask, PyQt (for GUI)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/FaceDataCollector.git
   cd FaceDataCollector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the client and server settings in their respective configuration files (`config.json`, `config.yaml`).

---

## 🚀 Usage
### Run the Server
1. Navigate to the `server` directory.
2. Start the server:
   ```bash
   python app.py
   ```

### Run the Client
1. Navigate to the `client` directory.
2. Start the client:
   ```bash
   python gui.py
   ```

---

## 🛠️ Features in Development
- Real-time feedback during video capture.
- Enhanced encryption for secure data transmission.
- Support for multi-client sessions.

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributions
Contributions are welcome! Please fork this repository and submit a pull request with your improvements.

---

## 📧 Contact
For questions or suggestions, please contact:
- **Name**: [Your Name]
- **Email**: [Your Email]
- **GitHub**: [Your GitHub Profile Link]
