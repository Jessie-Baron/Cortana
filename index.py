import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from threading import Thread
import os
import platform
import openai
from dotenv import load_dotenv
import speech_recognition as sr
import requests
from cortana import CortanaKnowledgeBase

class CortanaGUI(QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowTitle("Cortana")
        self.setGeometry(0, 0, 320, 200)  # Adjust the geometry as needed

        self.label = QLabel(self)
        # Set a smaller size for the label
        self.label.setGeometry(0, 0, 320, 200)

        # Load and display the image, scaled to the desired size
        monitor_size_inches = 22
        corner_size_inches = 3  # Adjust this value based on your preference
        pixels_per_inch = self.physicalDpiX()  # Get the pixels per inch of the screen
        desired_size_pixels = int(corner_size_inches * pixels_per_inch)

        pixmap = QPixmap(image_path).scaledToWidth(desired_size_pixels, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

        # Align the window to the bottom right of the screen
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry(desktop.primaryScreen())
        self.move(screen_rect.width() - self.width(), screen_rect.height() - self.height())

        self.show()


def main():
    # Example usage
    cortana_kb = CortanaKnowledgeBase()

    # Start a thread to listen for user input in the background
    listen_thread = Thread(target=lambda: listen_for_input(cortana_kb))
    listen_thread.daemon = True
    listen_thread.start()

    # Start the main loop
    app = QApplication(sys.argv)
    cortana_gui = CortanaGUI("/Users/jessiebaron/Downloads/cortana__halo_4__by_jr_rizzo_dehs90j-pre.jpg")  # Provide the path to the processed image
    sys.exit(app.exec_())


def listen_for_input(cortana_kb):
    while True:
        user_input = cortana_kb.recognize_speech()
        if user_input:
            response = cortana_kb.interact(user_input)
            cortana_kb.synthesize_audio(response)


if __name__ == "__main__":
    main()
