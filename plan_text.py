from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env file

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("List 5 planets each with an interesting fact", generation_config = genai.types.GenerationConfig(
                                  candidate_count = 1,
                                  stop_sequences = ['.'],
                                  max_output_tokens = 40,
                                  top_p = 0.6,
                                  top_k = 5,
                                  temperature = 0.8))


print(response.text)
