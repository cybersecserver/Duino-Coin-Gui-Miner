import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from PyQt6.QtCore import Qt

class MinerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Duino-Coin Miner")
        self.setGeometry(100, 100, 500, 500)
        self.setMinimumSize(400, 400)
        # Set window icon
        self.setWindowIcon(QIcon("icon.ico"))
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#23272f"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Modern fonts
        label_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        entry_font = QFont("Segoe UI", 11)
        button_font = QFont("Segoe UI", 12, QFont.Weight.Bold)

        # Title label
        self.title_label = QLabel("DUINO-MINER", self)
        self.title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #00b894; letter-spacing: 2px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Username
        self.label_user = QLabel("User Name", self)
        self.label_user.setFont(label_font)
        self.label_user.setStyleSheet("color: #f5f6fa;")
        self.entry_user = QLineEdit(self)
        self.entry_user.setFont(entry_font)
        self.entry_user.setFixedHeight(36)
        self.entry_user.setStyleSheet("""
            background: #2f3640;
            color: #f5f6fa;
            border: 1.5px solid #353b48;
            border-radius: 8px;
            padding-left: 10px;
        """)

        # Password
        self.label_pass = QLabel("Password", self)
        self.label_pass.setFont(label_font)
        self.label_pass.setStyleSheet("color: #f5f6fa;")
        self.entry_pass = QLineEdit(self)
        self.entry_pass.setFont(entry_font)
        self.entry_pass.setFixedHeight(36)
        self.entry_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.entry_pass.setStyleSheet("""
            background: #2f3640;
            color: #f5f6fa;
            border: 1.5px solid #353b48;
            border-radius: 8px;
            padding-left: 10px;
        """)

        # Mine button
        self.mine_button = QPushButton("Mine", self)
        self.mine_button.setFont(button_font)
        self.mine_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mine_button.setFixedHeight(40)
        self.mine_button.setStyleSheet("""
            QPushButton {
                background-color: #00b894;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 8px 0;
            }
            QPushButton:hover {
                background-color: #00cec9;
            }
        """)
        self.mine_button.clicked.connect(self.helloCallBack)

        # Layouts
        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.addWidget(self.title_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.label_user)
        form_layout.addWidget(self.entry_user)
        form_layout.addWidget(self.label_pass)
        form_layout.addWidget(self.entry_pass)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.mine_button)
        form_layout.setAlignment(self.mine_button, Qt.AlignmentFlag.AlignHCenter)

        # Center the form
        main_layout = QVBoxLayout()
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addLayout(form_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.setLayout(main_layout)

    def helloCallBack(self):
        import socket, hashlib, os, urllib.request
        soc = socket.socket()
        username = self.entry_user.text()
        password = self.entry_pass.text()
        serverip = "https://raw.githubusercontent.com/revoxhere/duino-coin/gh-pages/serverip.txt"
        try:
            with urllib.request.urlopen(serverip) as content:
                content = content.read().decode().splitlines()
            pool_address = content[0]
            pool_port = content[1]
            soc.connect((str(pool_address), int(pool_port)))
            server_version = soc.recv(3).decode()
            print("Server is on version", server_version)
            soc.send(bytes("LOGI," + username + "," + password, encoding="utf8"))
            response = soc.recv(2).decode()
            if response == "OK":
                print("Logged in")
            else:
                QMessageBox.critical(self, "Login Error", "Error logging in - check account credentials!")
                soc.close()
                os._exit(1)
            while True:
                soc.send(bytes("JOB", encoding="utf8"))
                job = soc.recv(1024).decode()
                job = job.split(",")
                difficulty = job[2]
                for result in range(100 * int(difficulty) + 1):
                    ducos1 = hashlib.sha1(str(job[0] + str(result)).encode("utf-8")).hexdigest()
                    if job[1] == ducos1:
                        soc.send(bytes(str(result), encoding="utf8"))
                        feedback = soc.recv(1024).decode()
                        if feedback == "GOOD":
                            print("Accepted share", result, "Difficulty", difficulty)
                            break
                        elif feedback == "BAD":
                            print("Rejected share", result, "Difficulty", difficulty)
                            break
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            soc.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinerWindow()
    window.show()
    sys.exit(app.exec())
