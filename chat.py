from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env file

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

chat_model = genai.GenerativeModel('gemini-pro')
chat = chat_model.start_chat(history=[])


response = chat.send_message("Which is one of the best place to visit in India during summer?")
print(response.text)
response = chat.send_message("Tell me more about that place in 50 words")
print(response.text)

print(chat.history)  