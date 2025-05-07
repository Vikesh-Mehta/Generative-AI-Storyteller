# Generative AI Storyteller 📚✨

Welcome to the Generative AI Storyteller! This web application allows users to kickstart their creative writing process by providing an initial story prompt. Our AI, powered by Google's Gemini API, then generates a creative and contextually relevant continuation of the narrative.

This project serves as a demonstration of how Large Language Models (LLMs) can be integrated into web applications to provide engaging and useful tools for creativity and entertainment.

## Features

*   **Interactive Story Prompting:** Users can input any starting sentence or paragraph.
*   **AI-Powered Continuation:** Leverages Google's Gemini API (specifically `gemini-1.5-flash-latest` or similar) to generate story continuations.
*   **User-Friendly Web Interface:** Clean and simple UI built with HTML, CSS, and JavaScript.
*   **Real-time Feedback:** Loading indicators and clear error messages.
*   **Secure API Key Management:** Uses environment variables for API key storage.
*   **Responsive Design (Basic):** Usable on desktop browsers.

## Project Structure

generative_storyteller_gemini/
├── .env # Stores API keys and environment variables (NOT COMMITTED)
├── .gitignore # Specifies intentionally untracked files that Git should ignore
├── app.py # Flask backend application (API logic, Gemini integration)
├── requirements.txt # Python dependencies
├── static/ # Static files (CSS, JS, images)
│ └── style.css # CSS for styling the frontend
└── templates/ # HTML templates for Flask
└── index.html # Main HTML page for the application



## Technologies Used

*   **Frontend:**
    *   HTML5
    *   CSS3
    *   JavaScript (ES6+)
*   **Backend:**
    *   Python 3.8+
    *   Flask (Micro web framework)
*   **Generative AI:**
    *   Google Gemini API (e.g., `gemini-1.5-flash-latest` model)
    *   `google-generativeai` Python SDK
*   **API Key Management:**
    *   `.env` files
    *   `python-dotenv` library
*   **Development Environment:**
    *   Python Virtual Environment (`venv`)
*   **Version Control:**
    *   Git & GitHub

## Setup and Installation

Follow these steps to get the project running locally:

**1. Clone the Repository:**

   ```bash
   git clone https:https://github.com/Vikesh-Mehta/Generative-AI-Storyteller.git
   cd generative-storyteller-gemini

2. Create and Activate a Python Virtual Environment:
On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies:
Make sure you are in the project root directory (where requirements.txt is located).
pip install -r requirements.txt

4. Set up Environment Variables (API Key):
You need a Google Gemini API Key. You can obtain one from Google AI Studio.
Create a file named .env in the root of your project directory.
Add your API key and Flask settings to the .env file:
```env
 GOOGLE_API_KEY=your_actual_google_api_key_here
 FLASK_APP=app.py
 FLASK_DEBUG=True
 ```
 **Important:** Replace `your_actual_google_api_key_here` with your real API key. The `.gitignore` file is already configured to prevent this file from being committed to Git.

5. Run the Application:
With your virtual environment activated and the .env file configured:
flask run --host=0.0.0.0 --port=5000
OR python app.py
