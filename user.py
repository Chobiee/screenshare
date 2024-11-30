import socket
import pyautogui
import pickle
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import sys


class UserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Screen Sharing")

        # Start Sharing Button
        self.start_button = QPushButton("Start Sharing")
        self.start_button.clicked.connect(self.start_sharing)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start_sharing(self):
        # Set up the socket
        host = '127.0.0.1'  # Replace with Admin's IP Address
        port = 5001

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
                print("Connected to Admin.")
                while True:
                    # Capture the screen
                    screenshot = pyautogui.screenshot()
                    data = pickle.dumps(screenshot)

                    # Send the data
                    s.sendall(data)
            except ConnectionRefusedError:
                print("Connection refused. Ensure Admin App is running and reachable.")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_app = UserApp()
    user_app.show()
    sys.exit(app.exec_())
