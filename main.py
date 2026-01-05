import google.generativeai as genai
import os

# Ensure your key is set in your environment or paste it here
api_key = os.getenv("GOOGLE_API_KEY") 
genai.configure(api_key=api_key)

print("My Available Models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")
