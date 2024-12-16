from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction
import sys

class server(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 600 , 400)
        self.setWindowTitle("FeaceCaptureNetWork Server")
        self.setup_Tab()
    
    def setup_Tab(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout()

        # setup panel
        self.setup_leftPanel()
        self.setup_rightPanel()

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.VLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)

        self.main_layout.addLayout(self.left_panel, 1)
        self.main_layout.addWidget(self.divider)
        self.main_layout.addLayout(self.right_panel,3)


        
    def setup_leftPanel(self):
        self.left_panel = QVBoxLayout()

        self.sessions_Working_button = QPushButton("Sessions Working", self)
        self.sessions_Working_button.clicked.connect(self.setup_workingPage)

        self.sessions_Worked_button = QPushButton("Sessions Worked", self)
        self.sessions_Worked_button.clicked.connect(self.setup_workedPage)

        self.connection_requested_button = QPushButton("Conection Requested", self)
        self.connection_requested_button.clicked.connect(self.list_connected)

        self.manage_sessions_button = QPushButton("Manage Sessions")
        self.manage_sessions_button.clicked.connect(self.show_manage_sessions)

        self.left_panel.addWidget(self.sessions_Working_button)
        self.left_panel.addWidget(self.sessions_Worked_button)
        self.left_panel.addWidget(self.connection_requested_button)
        self.left_panel.addWidget(self.manage_sessions_button)

        
    def setup_workingPage(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("List of session working"))
        
        self.session_table = QTableWidget(5, )
        self.session_table.setHorizontalHeaderLabels(["Session ID", "Client"])
        layout.addWidget(self.session_table)
        self.session_working_tab.setLayout(layout)
    

    def setup_workedPage(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Worked Session"))

        self.worked_table = QTableWidget(5,3)
        self.worked_table.setHorizontalHeaderLabels(["Date", "Client" , "Status"])
        layout.addWidget(self.worked_table)
        self.session_worked_tab.setLayout(layout)

    def list_connection_requested(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("List Connection Requested"))
        
        self.list_requested_tabel = QTableWidget(5,3)
        self.list_requested_tabel.setHorizontalHeaderLabels(["Time", "Client Address", "Status"])
        layout.addWidget(self.list_requested_tabel)
        self.connection_requested_tab.setLayout(layout)

    def show_manage_sessions(self):
        print(4)

#-------------------------------------------------------------------- Set up Right Panel ---------------------------------------------------------------------
    def setup_rightPanel(self):
        self.session_working_tab = QWidget()
        self.session_worked_tab = QWidget()
        self.connection_requested_tab = QWidget()
        self.manage_session_tab = QWidget()
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window  = server()
    window.show()
    sys.exit(app.exec())





