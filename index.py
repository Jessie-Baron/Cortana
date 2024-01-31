import sys
from PyQt5.QtWidgets import QApplication
from threading import Thread
from cortana import CortanaKnowledgeBase
from model import CortanaGUI

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
