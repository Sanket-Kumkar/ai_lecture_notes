import google.generativeai as genai

genai.configure(api_key="AIzaSyAB9tUMDK9kz2lRwJ_4ebXdDym8T3A7I-8")

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
