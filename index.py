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

# Load environment variables from .env
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.environ.get('CORTANA_INDEX')


class CortanaKnowledgeBase:
    def __init__(self):
        # Initialize a knowledge base with information about Cortana
        self.cortana_info = {
            "name": "Cortana",
            "personality_traits": ["intelligent", "witty", "curious", "supportive"],
            "background": "Cortana is an advanced AI construct created by Dr. Halsey...",
            "quotes": [
                "I am your shield. I am your sword.",
                "Don't make a girl a promise if you know you can't keep it.",
                # Add more iconic quotes
            ],
            # Add more details as needed
        }
        self.context = []

    def get_cortana_info(self, aspect=None):
        if aspect:
            return self.cortana_info.get(aspect, "Information not available.")
        else:
            return self.cortana_info

    def generate_cortana_response(self, user_input):
        # Custom logic to generate responses based on user input
        if "how are you" in user_input.lower():
            return "I'm an AI, so I don't experience emotions, but thanks for asking."

        elif "what is your purpose" in user_input.lower():
            return "I am an aartificial intelligence construct. I was one of the most important figures in the Human-Covenant war, and was John-117's partner in various combat missions as well as serving as the AI for the Halcyon-class light cruiser - UNSC Pillar of Autumn, Orbital Defense Platform - Cairo Station Charon-class light frigate - UNSC Forward Unto Dawn, and Stalwart-class light frigate UNSC In Amber Clad. In addition, I hold vital data pertaining to the Halos, including the Activation Index from Installation 04. Now I am just your personal AI assistant!"

        # Add more custom response patterns as needed

        # If no specific pattern matches, use GPT-3 for general conversation
        return self.generate_gpt3_response(user_input)

    def generate_gpt3_response(self, user_input):
        # Prepare the conversation history for GPT-3
        conversation_history = [{"role": "user", "content": u["content"]} for u in self.context]

        # Use OpenAI GPT-3 for general conversation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            max_tokens=150,  # Adjust as needed
            temperature=0.7  # Adjust for randomness in responses (0.0 to 1.0)
        )['choices'][0]['message']['content'].strip()

        return response

    def interact(self, user_input):
        # Update the context with user input
        self.context.append({"role": "user", "content": user_input})

        # If the user asks about Cortana, provide information
        if "tell me about yourself" in user_input.lower():
            response = self.get_cortana_info()
            if isinstance(response, dict):
                return response  # Return the dictionary directly
            else:
                return f"Cortana says: {response}"  # Format the string response
        else:
            # Generate a response with Cortana's personality
            response = self.generate_cortana_response(user_input)

        # Update the context with Cortana's response
        self.context.append({"role": "assistant", "content": response})

        return response

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error connecting to Google API: {e}")
            return None

    def synthesize_audio(self, text):
        url = "https://api.elevenlabs.io/v1/text-to-speech/SLPZrQfiDYD7GygGgA2c"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": os.environ.get('CORTANA_VOICE')
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
        }

        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the synthesized audio to a file
            with open("cortana_response.mp3", "wb") as f:
                f.write(response.content)

            # Play the synthesized audio
            try:
                if platform.system() == "Darwin":  # macOS
                    os.system("afplay cortana_response.mp3")
                elif platform.system() == "Windows":
                    os.system("start cortana_response.mp3")
                elif platform.system() == "Linux":
                    os.system("xdg-open cortana_response.mp3")
            except Exception as e:
                print(f"Error playing audio: {e}")
        else:
            print(f"Error: {response.status_code} - {response.text}")


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
