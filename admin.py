import socket
import pickle
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QLineEdit, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sys


class AdminApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.server_socket = None
        self.client_socket = None
        self.client_address = None

    def init_ui(self):
        self.setWindowTitle("Admin Screen Viewer")

        # GUI components
        self.image_label = QLabel("Waiting for screen data...")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter User's IP Address")

        self.start_button = QPushButton("Start Viewing")
        self.start_button.clicked.connect(self.start_server)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.ip_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def start_server(self):
        # Get the IP from the input box
        host = self.ip_input.text()
        port = 5001

        if not host:
            self.image_label.setText("Please enter a valid IP address.")
            return

        # Set up the server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.image_label.setText("Waiting for connection...")

        self.client_socket, self.client_address = self.server_socket.accept()
        self.image_label.setText(f"Connected to: {self.client_address[0]}")
        print(f"Connection established with: {self.client_address}")

        self.receive_data()

    def receive_data(self):
        while True:
            try:
                data = b""
                while True:
                    packet = self.client_socket.recv(4096)
                    if not packet:
                        break
                    data += packet

                # Deserialize the image data
                screenshot = pickle.loads(data)
                screenshot = screenshot.convert("RGB")
                img = screenshot.toqimage()
                pixmap = QPixmap.fromImage(QImage(img))

                self.image_label.setPixmap(pixmap)
            except Exception as e:
                print(f"Error: {e}")
                break

        self.client_socket.close()
        self.server_socket.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    admin_app = AdminApp()
    admin_app.show()
    sys.exit(app.exec_())
