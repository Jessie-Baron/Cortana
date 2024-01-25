import openai
import os

# Set your OpenAI API key
openai.api_key = os.environ.get('CORTANA_INDEX')

class CortanaAssistant:
    def __init__(self):
        self.name = "Cortana"
        self.user_name = None
        self.context = []

    def ask_openai(self, question):
        # Use the OpenAI GPT-3 model to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.context
        )
        return response['choices'][0]['message']['content'].strip()

    def interact(self, user_input):
        # Update the context with user input
        self.context.append({"role": "user", "content": user_input})

        # If the user provides their name, remember it
        if "my name is" in user_input.lower():
            self.user_name = user_input.lower().replace("my name is", "").strip()

        # Get response from OpenAI
        response = self.ask_openai(user_input)

        # Update the context with the assistant's response
        self.context.append({"role": "assistant", "content": response})

        return response

    def introduce(self):
        if self.user_name:
            return f"Hello, {self.user_name}! I'm {self.name}, your virtual assistant. How can I assist you today?"
        else:
            return f"I'm {self.name}, your virtual assistant. What's your name?"

# Example usage
cortana = CortanaAssistant()

user_input = input("You: ")
while user_input.lower() != 'exit':
    if "what is your name" in user_input.lower():
        response = cortana.introduce()
    else:
        response = cortana.interact(user_input)

    print(f"{cortana.name}: {response}")
    user_input = input("You: ")
