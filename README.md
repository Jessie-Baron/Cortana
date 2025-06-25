# 🧠 Cortana AI Assistant (Desktop Edition)

Cortana is a Halo-inspired AI voice assistant that speaks with personality, checks your Gmail inbox, and can open long emails in a browser. With voice-based input, real-time speech synthesis, and smart email filtering, Cortana is your desktop companion brought to life.

---

## 🎯 Features

- 🎙️ Listens to your voice and interprets prompts
- 💌 Fetches and reads your latest email from the *Primary Inbox*
- 🧠 Responds to general questions using OpenAI's GPT
- 🌐 (Optional) Opens long responses in the browser
- 🖼️ Displays Cortana in a stylish bottom-corner GUI window

---
## Watch a Demo of Cortana
🎥 [HERE](https://jessie-redshift-bucket.s3.us-east-1.amazonaws.com/Screen+Recording+2025-06-25+at+7.23.52+PM.mov)

## 📸 Screenshots

Cortana Desktop GUI

<img width="317" alt="Screenshot 2025-06-25 at 7 38 39 PM" src="https://github.com/user-attachments/assets/c0944c77-d321-4b5f-9b92-6409d8243cf8" />

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cortana-assistant.git
cd cortana-assistant
```

## 2. Install Dependencies
Make sure you’re using Python 3.9+ and install required packages:

```bash
pip install -r requirements.txt
```

## 3. Setup Environment Variables
Create a .env file at the root of your project:

```
CORTANA_INDEX=your_openai_api_key # You can aquire an openapi key at openapi.com
CORTANA_VOICE=your_elevenlabs_api_key # You can aquire an elevenlabs api key at el;evenlabs.com
```

## 4. Provide Cortana's Image
Place a Cortana-themed image in the ./assets or project directory, and update the path in index.py:

```
CortanaGUI("/Users/yourname/path/to/image.jpg")
```

## 🚀 Running the App
python index.py

Cortana will begin listening for your voice commands and display her image in the bottom right corner of your screen.

## 📬 Email Integration Notes
Only emails from the Primary Inbox are read.

Emails longer than 100 characters are saved to email_body.html and opened in your default browser.

## 💡 Future Improvements
Add Bing or Google Search API integration

Let users customize Cortana’s voice and background

Add task scheduling or calendar integration
