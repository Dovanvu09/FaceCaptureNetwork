from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QColor, QImage,QPixmap
import sys
import cv2
import ctypes

client_lib = ctypes.CDLL('C:/Users/dvuAI/THLTM_Project/libclient.so')

# Khai báo các phương thức từ thư viện C++
client_new = client_lib.client_new
client_new.argtypes = [ctypes.c_char_p, ctypes.c_int]
client_new.restype = ctypes.POINTER(ctypes.c_void_p)

client_delete = client_lib.client_delete
client_delete.argtypes = [ctypes.POINTER(ctypes.c_void_p)]

client_send_image = client_lib.client_send_image
client_send_image.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]

client_receive_image_and_decompress = client_lib.client_receive_image_and_decompress
client_receive_image_and_decompress.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]

client_send_request_to_view_images = client_lib.client_send_request_to_view_images
client_send_request_to_view_images.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p, ctypes.c_char_p]



class Home_User(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_UI()
    
    def initialize_UI(self):
        self.setGeometry(100, 100, 600,400)
        self.setWindowTitle("FaceCaptureNetwork")
        
        self.setup_menubar()
        self.setup_Tab()
        self.apply_styles()
    # Setup tab
    def setup_Tab(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your Name:")
        self.name_input.setFixedSize(130,40)
        self.name_input.setFont(QFont("Arial =", 12))

        self.submit_button = QPushButton("Submit and Open Camera")
        self.submit_button.setFixedSize(200,50)
        self.submit_button.clicked.connect(self.open_camera)

        self.main_layout.addStretch()
        self.main_layout.addWidget(self.name_input, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.submit_button, alignment = Qt.AlignmentFlag.AlignCenter)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.addStretch()
    
    def setup_menubar(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")

        #Add action to control 
        fps_action = QAction("Set Fps", self)
        fps_action.triggered.connect(self.set_fps)
        settings_menu.addAction(fps_action)

        resolution_action = QAction("Set Resolution", self)
        resolution_action.triggered.connect(self.set_resolution)
        settings_menu.addAction(resolution_action)

        logout_action = QAction("Logout",self)
        logout_action.triggered.connect(self.logout)
        settings_menu.addAction(logout_action)

        session_worked = QAction("Session Worked",self)
        session_worked.triggered.connect(self.Review)
        settings_menu.addAction(session_worked)

#------------------------------------------- set and update resolution ---------------------------------------------
    def set_resolution(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("set Resolution")
        dialog.resize(150,100)
        dialog_layout = QVBoxLayout()

        self.resolution_label = QLabel("Resolution : ")
        self.resolution_input = QComboBox(self)
        self.resolution_input.addItems(["1080x1920", "720x1280", "540x960"])
        self.resolution_input.setFixedSize(130,40)
        self.resolution_input.setCurrentIndex(0)

        self.set_button = QPushButton("Set", dialog)
        self.set_button.clicked.connect(lambda: self.update_resolution(dialog))
        self.cancel_button = QPushButton("Cancel", dialog)
        self.cancel_button.clicked.connect(dialog.accept)
        # Button Action
        dialog_layout.addWidget(self.resolution_label)
        dialog_layout.addWidget(self.resolution_input)
        dialog_layout.addWidget(self.set_button)
        dialog_layout.addWidget(self.cancel_button)

        dialog.setLayout(dialog_layout)
        dialog.exec()
    def update_resolution(self, dialog):
        selected_resolution = self.resolution_input.currentText()
        QMessageBox.information(self, "Success", f"Resolution set to{selected_resolution}", QMessageBox.StandardButton.Ok)
        dialog.accept()
#----------------------------------------------- set and update fps --------------------------------------------------
    def set_fps(self):
        # show a pop-up to input the FPS value
        dialog = QDialog(self)
        dialog.setWindowTitle("Set FPS")
        dialog.resize(150,100)
        #Layout for the dialog
        dialog_layout = QVBoxLayout()

        self.fps_label = QLabel("Enter FPS: ")
        self.fps_input = QSpinBox(dialog)
        self.fps_input.setRange(10, 60)
        self.fps_input.setValue(30)

        self.set_button = QPushButton("Set", dialog)
        self.cancel_button = QPushButton("Cancel", dialog)
        #Button actions 
        self.set_button.clicked.connect(lambda: self.update_fps(self.fps_input.value(), dialog))
        self.cancel_button.clicked.connect(dialog.reject)

        dialog_layout.addWidget(self.fps_label)
        dialog_layout.addWidget(self.fps_input)
        dialog_layout.addWidget(self.set_button)
        dialog_layout.addWidget(self.cancel_button)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def update_fps(self, value, dialog):
        self.fps_input.setValue(value)
        QMessageBox.information(self, "Succes", f"fps set to {value}",QMessageBox.StandardButton.Ok)
        dialog.accept()
# ------------------------------------------------------Open camera and visualize image ------------------------------------------------
    def open_camera(self):
        faces_data = []
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.show_Error("Error: Could not open camera")
            return

        # get resolution
        resolution = self.resolution_input.currentText()
        width, height = self.get_resolution(resolution)

        # set resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        cascade_path = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
        count = 0
        while True:
            ok , frame = cap.read()
            faces = cascade_path.detectMultiScale(frame, 1.3, 5)
            for(x, y, w, h) in faces:
                margin = 0.2
                x = int(x - margin * w)  # Giảm x để mở rộng vùng sang trái
                y = int(y - margin * h)  # Giảm y để mở rộng vùng lên trên
                w = int(w * (1 + 2 * margin))  # Tăng chiều rộng của khuôn mặt lên 20%
                h = int(h * (1 + 2 * margin))  # Tăng chiều cao của khuôn mặt lên 20%

                # Đảm bảo không vượt quá biên giới của khung hình
                x = max(x, 0)
                y = max(y, 0)
                w = min(w, frame.shape[1] - x)
                h = min(h, frame.shape[0] - y)
                cv2.rectangle(frame, (x,y), (x+w, y+h),(255, 0, 0), 2)
                img = cv2.resize(frame[y+2:y+h-2, x+2 : x+w-2],(width, height))
                faces_data.append(img)
                count += 1
                cv2.imshow('Frame', frame)
            if count == 100:
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        

        cap.release()
        cv2.destroyAllWindows()
        self.display_faces(faces_data)
    def display_faces(self, faces_data):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dectected Faces")
        dialog.resize(800,600)

        face_layout = QGridLayout()
        rows = 10
        cols = 10
        max_faces = rows*cols
        faces_data = faces_data[:max_faces]

        widget_width = dialog.width()
        widget_height = dialog.height()

        cell_width = widget_width // cols
        cell_height = widget_height // rows

        for i, face in enumerate(faces_data):
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

            height, width, channel = face_rgb.shape
            bytes_per_line = 3 * width
            qimg = QImage(face_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

            pixmap = QPixmap.fromImage(qimg)
            scaled_pixmap = pixmap.scaled(cell_width, cell_height, Qt.AspectRatioMode.KeepAspectRatio)

            face_label = QLabel()
            face_label.setPixmap(scaled_pixmap)
            face_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            info_label = QLabel(f"Face {i+1}")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            face_widget = QWidget()
            face_layout_widget = QVBoxLayout()
            face_layout_widget.addWidget(face_label)
            face_layout_widget.addWidget(info_label)

            face_widget.setLayout(face_layout_widget)

            row = i // cols
            col = i % rows
            face_layout .addWidget(face_widget, row, col)
        
        self.sendButton = QPushButton("Send")
        self.sendButton.resize(100,60)
        face_layout.addWidget(self.sendButton, rows, cols // 2)
        self.sendButton.clicked.connect(self.send_Image_to_Server)
        
        # creat a QWidget contain layout face_layout
        scroll_widget = QWidget()
        scroll_widget.setLayout(face_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(scroll_area)

        dialog.setLayout(dialog_layout) 
        dialog.exec()
#------------------------------------------------------------ view session worked and log out ---------------------------------------------------------
    def Review(self):
        print("Session worked")

    def logout(self):
        from Login import LoginWindow
        self.logout_window = LoginWindow()
        self.logout_window.show()
        self.close()
    
# --------------------------------- ----------------------------other function ---------------------------------------------------
    def get_resolution(self,resolution):
        if resolution == "1920x1080":
            return 1920, 1080
        
        elif resolution == "1280x720":
            return 1280, 720
        
        elif resolution == "640x480":
            return 640, 480
        
        else:
            return 640, 480
    
    def send_Image_to_Server(self):
        print("Hello server")

    def apply_styles(self):
        """Apply styles to the widgets."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #003865;
            }
            QLineEdit {
                border: 2px solid #0078d7;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLabel {
                color: #333333;
            }
        """)
    def show_message(self, title, message):
        QMessageBox.information(self,title,message,QMessageBox.StandardButton.Ok)
    
    def show_Error(self, message):
        QMessageBox.critical(self,"Error", message, QMessageBox.StandardButton.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home_User()
    window.show()
    sys.exit(app.exec())