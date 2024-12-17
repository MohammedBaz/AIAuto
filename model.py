import google.generativeai as genai

# Configure and load the Gemini model
def configure_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

# Function to generate content based on a prompt
def generate_response(model, prompt):
    response = model.generate_content(prompt)
    return response.text  # Return the response text
