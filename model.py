from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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
