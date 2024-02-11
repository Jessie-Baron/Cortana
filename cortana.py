import os
import platform
import openai
from dotenv import load_dotenv
import speech_recognition as sr
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow  # Added this import
import base64
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import webbrowser

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
            return "I am an artificial intelligence construct. I was one of the most important figures in the Human-Covenant war, and was John-117's partner in various combat missions as well as serving as the AI for the Halcyon-class light cruiser - UNSC Pillar of Autumn, Orbital Defense Platform - Cairo Station Charon-class light frigate - UNSC Forward Unto Dawn, and Stalwart-class light frigate UNSC In Amber Clad. In addition, I hold vital data pertaining to the Halos, including the Activation Index from Installation 04. Now I am just your personal AI assistant!"

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

    def authenticate_gmail_api(self):
        creds = None
        token_path = os.environ.get('CORTANA_GMAIL_INDEX')  # Change to your token file path
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.environ.get('CORTANA_ID_REFERENCE'), ['https://www.googleapis.com/auth/gmail.readonly'])
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_latest_email(self):
        creds = self.authenticate_gmail_api()
        service = build('gmail', 'v1', credentials=creds)

        # Get the list of messages
        messages = service.users().messages().list(userId='me', labelIds=['INBOX', 'CATEGORY_PERSONAL']).execute()
        if 'messages' in messages:
            latest_message_id = messages['messages'][0]['id']
            message = service.users().messages().get(userId='me', id=latest_message_id).execute()

            # Extract email subject
            subject = next(header['value'] for header in message['payload']['headers'] if header['name'] == 'Subject')

            # Check if 'parts' key is present
            if 'parts' in message['payload']:
                # Extract email body from 'parts' key
                body = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data']).decode('utf-8')
            else:
                # If 'parts' key is not present, try to access the 'body' directly
                body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
            # Use BeautifulSoup to strip HTML tags
            soup = BeautifulSoup(body, 'html.parser')
            plain_text_body = soup.get_text()

            # Check character limit
            character_limit = 100  # Set your desired character limit
            if len(plain_text_body) > character_limit:
                # If email body exceeds the character limit, save it to a file
                output_file_path = 'email_body.html'
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(body)

                # Open the file in a new browser window
                webbrowser.open(f'file://{os.path.abspath(output_file_path)}')
                return "Opening the email in a new browser window."

            return f"Latest email: Subject - {subject}, Body - {plain_text_body}"

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

        if "check my email" in user_input.lower():
            email_notification = self.get_latest_email()
            return email_notification
        elif "open my email" in user_input.lower():
            # Add logic to open the email in a browser
            return "Opening your email in a browser."
        else:
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

        # Split the text into chunks of 5000 characters
        chunks = [text[i:i + 5000] for i in range(0, len(text), 5000)]

        # Initialize an empty list to store audio content
        audio_content_list = []

        for chunk in chunks:
            data = {
                "text": chunk,  # Fix the typo here; it should be 'chunk' instead of 'text'
                "model_id": "eleven_multilingual_v2",
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                # Append the audio content to the list
                audio_content_list.append(response.content)
            else:
                print(f"Error: {response.status_code} - {response.text}")

        # Combine the audio content from all chunks
        combined_audio_content = b''.join(audio_content_list)

        # Save the synthesized audio to a file
        with open("cortana_response.mp3", "wb") as f:
            f.write(combined_audio_content)

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
