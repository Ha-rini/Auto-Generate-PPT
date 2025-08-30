# MultipleFiles/llm_services.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_slide_content(prompt: str) -> str:
    """
    Generates slide content using the Aipipe API.
    """
    # Get the Aipipe token from the environment variable
    # Aipipe uses OPENAI_API_KEY for its token
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Define the Aipipe API endpoint for chat completions
    # Based on https://github.com/sanand0/aipipe?tab=readme-ov-file#api
    url = "https://aipipe.org/openai/v1/chat/completions"

    # Set up the headers for the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Set up the payload for the API request
    # Aipipe expects a messages array for chat completions
    payload = {
        "model": "openai/gpt-4o-mini",  # Or another model supported by Aipipe
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates concise slide content."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300, # Increased max_tokens for potentially more content per slide
        "temperature": 0.7
    }

    try:
        # Make the API request
        response = requests.post(url, headers=headers, json=payload, timeout=60) # Added timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # Adjust based on the actual response structure for chat completions
        # The response structure for chat completions is data['choices'][0]['message']['content']
        if data and 'choices' in data and len(data['choices']) > 0 and 'message' in data['choices'][0] and 'content' in data['choices'][0]['message']:
            return data['choices'][0]['message']['content']
        else:
            print(f"Error: Unexpected response structure from Aipipe: {data}")
            return "Error: Could not parse content from Aipipe response."

    except requests.exceptions.Timeout:
        print("Error: Aipipe API request timed out.")
        return "Error: Aipipe API request timed out."
    except requests.exceptions.RequestException as e:
        print(f"Error: Aipipe API request failed: {e}")
        return f"Error: Aipipe API request failed: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

