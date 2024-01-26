import openai
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import os


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

    def speak_text(self, response):
        if isinstance(response, dict):
            # Extract relevant information from the dictionary
            name = response.get("name", "Cortana")
            personality_traits = ", ".join(response.get("personality_traits", []))
            background = response.get("background", "Information not available.")

            # Generate a response string
            response_text = f"I am {name}, an AI with the following traits: {personality_traits}. {background}"
        else:
            response_text = response

        # Use gTTS to convert the response text into speech
        tts = gTTS(text=response_text, lang='en')
        tts.save("cortana_response.mp3")

        # Use the 'open' command to play the MP3 file on macOS
        try:
            os.system("open cortana_response.mp3")
        except Exception as e:
            print(f"Error playing audio: {e}")

    def interact_with_speech(self):
        user_input = self.recognize_speech()
        if user_input:
            response = self.interact(user_input)
            self.speak_text(response)

# Example usage
cortana_kb = CortanaKnowledgeBase()

while True:
    cortana_kb.interact_with_speech()
