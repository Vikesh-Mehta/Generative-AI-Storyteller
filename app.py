from flask import Flask, request, jsonify, render_template
import google.generativeai as genai # Changed import
import os
from dotenv import load_dotenv
import logging # For better error logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Google Gemini API key
google_api_key = os.getenv("GOOGLE_API_KEY") # Changed variable name
if not google_api_key:
    logger.error("Error: GOOGLE_API_KEY environment variable not set.")
    # Application might not function correctly without the API key
else:
    try:
        genai.configure(api_key=google_api_key)
        logger.info("Google Gemini API key configured.")
    except Exception as e:
        logger.error(f"Error configuring Google Gemini API: {e}")
        google_api_key = None # Ensure it's None if configuration fails

# Initialize the GenerativeModel (you can choose your model)
# Let's use a common one like 'gemini-1.5-flash-latest' or 'gemini-pro'
# 'gemini-1.5-flash-latest' is good for speed and often available on free tiers.
# 'gemini-pro' is also a solid choice.
MODEL_NAME = "gemini-1.5-flash-latest" # Or "gemini-pro"
try:
    if google_api_key: # Only attempt to initialize model if API key was set
        model = genai.GenerativeModel(MODEL_NAME)
        logger.info(f"Google Gemini model '{MODEL_NAME}' initialized.")
    else:
        model = None
        logger.warning("Google Gemini model not initialized due to missing API key.")
except Exception as e:
    logger.error(f"Error initializing Google Gemini model '{MODEL_NAME}': {e}")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story_api():
    if not google_api_key:
        return jsonify({"error": "Google API key not configured on the server."}), 500
    if not model:
        return jsonify({"error": f"Google Gemini model '{MODEL_NAME}' not initialized. Check server logs."}), 500

    try:
        data = request.get_json()
        user_prompt = data.get('prompt') # Renamed to avoid conflict with any internal 'prompt'

        if not user_prompt:
            return jsonify({"error": "Prompt is missing"}), 400

        if len(user_prompt) > 2000: # Adjust as needed, Gemini has token limits
            return jsonify({"error": "Prompt is too long (max 2000 characters for this demo)"}), 400

        # --- Google Gemini API Call ---
        # Construct a more instructive prompt for the model
        full_prompt = f"""You are a creative storyteller.
User's story starter: "{user_prompt}"
Continue this story, making it engaging and imaginative. Keep the continuation concise, around 150-200 words.
Story continuation:"""

        try:
            # Generation configuration (optional, but good for control)
            generation_config = genai.types.GenerationConfig(
                # candidate_count=1, # Default is 1
                # stop_sequences=['\n\n\n'], # Example: stop if three newlines occur
                max_output_tokens=300, # Max tokens for the generated text
                temperature=0.8,      # Controls randomness. Higher is more creative.
                top_p=0.95,
                top_k=40
            )

            # Safety settings (optional, defaults are usually sensible)
            # You can adjust these if you encounter content blocking frequently for benign prompts.
            # safety_settings = [
            #     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            #     {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            #     {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            #     {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            # ]

            response = model.generate_content(
                full_prompt,
                generation_config=generation_config,
                # safety_settings=safety_settings # Uncomment to use custom safety settings
            )
            
            # Check for safety blocks or empty response
            if not response.candidates:
                 # This can happen if all candidates were filtered due to safety or other reasons.
                 block_reason_msg = "Content generation blocked. The prompt might have violated safety guidelines or resulted in no valid output."
                 if response.prompt_feedback and response.prompt_feedback.block_reason:
                     block_reason_msg = f"Content generation blocked due to: {response.prompt_feedback.block_reason.name}"
                 logger.warning(f"Gemini response blocked or empty. Prompt: '{user_prompt}'. Reason: {block_reason_msg}")
                 return jsonify({"error": block_reason_msg}), 400 # Bad Request as prompt might be the issue

            # Assuming we take the first candidate (usually there's only one unless candidate_count > 1)
            story_continuation = response.text.strip()

            if not story_continuation: # If text is empty string
                story_continuation = "The AI couldn't come up with a story continuation this time. Try a different prompt!"


        # Handle API specific errors from google-generativeai
        # The SDK might raise various exceptions, e.g., from google.api_core.exceptions
        # For simplicity, catching a general exception here, but you can get more specific.
        except Exception as e_gemini: # Catching general exception for API calls
            logger.error(f"Error during Google Gemini API call: {e_gemini}", exc_info=True)
            # Try to get a more user-friendly message if possible
            error_message = str(e_gemini)
            if hasattr(e_gemini, 'message'): # Some Google API errors have a 'message' attribute
                 error_message = e_gemini.message
            
            status_code = 500 # Internal Server Error
            # Check for common API error types if possible (pseudo-code, actual exceptions may vary)
            if "API key not valid" in error_message or "PermissionDenied" in str(type(e_gemini)):
                error_message = "Authentication with Google AI service failed. Check your API key."
                status_code = 401 # Unauthorized
            elif "Quota" in error_message or "ResourceExhausted" in str(type(e_gemini)):
                error_message = "Google AI service quota exceeded. Please check your usage or try again later."
                status_code = 429 # Too Many Requests
            elif "Invalid" in error_message or "BadRequest" in str(type(e_gemini)): # e.g. model not found
                error_message = f"Invalid request to Google AI service: {error_message}"
                status_code = 400 # Bad Request

            return jsonify({"error": f"An error occurred with the Google AI service: {error_message}"}), status_code
        # --- End Google Gemini API Call ---

        return jsonify({"story": story_continuation})

    except Exception as e:
        logger.error(f"Error in /generate_story endpoint: {e}", exc_info=True)
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    if not google_api_key:
        logger.warning("CRITICAL: GOOGLE_API_KEY is not set. The application will not be able to contact the Gemini API.")
    if not model:
        logger.warning(f"CRITICAL: Google Gemini model '{MODEL_NAME}' failed to initialize. Story generation will not work.")
    
    # For development, Flask's built-in server is fine.
    # debug=True is handled by FLASK_DEBUG in .env if python-dotenv is used with `flask run`
    # If running directly with `python app.py`, set debug explicitly or rely on FLASK_DEBUG.
    app.run(host='0.0.0.0', port=5000, debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")