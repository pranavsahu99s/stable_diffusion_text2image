import os
import requests
import uuid
import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from threading import Lock  # Import the threading Lock

# --- 1. Load Keys and Set Up Global State ---
load_dotenv()

# Load the comma-separated keys from .env
API_KEYS_STRING = os.getenv("STABILITY_KEYS")
if not API_KEYS_STRING:
    raise ValueError("STABILITY_KEYS not found in .env. Please add them as a comma-separated list.")

# Create our list of keys
api_keys = [key.strip() for key in API_KEYS_STRING.split(',')]
if not api_keys:
    raise ValueError("No API keys found in STABILITY_KEYS.")

print(f"Loaded {len(api_keys)} API keys.")

# Global variables to track the current key
current_key_index = 0
# A Lock to prevent race conditions if multiple users request at once
key_lock = Lock()

# --- End of New Setup ---


# Initialize the Flask app
app = Flask(__name__)


# --- 2. Modified Colab Function ---
# It now requires an 'api_key' to be passed in
def send_generation_request(host, params, api_key):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {api_key}" # Use the provided key
    }
    files = {"none": ''}
    
    print(f"Sending REST request to {host}...")
    
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    
    if not response.ok:
        # Raise an exception with the exact error message from the API
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response
# --- End of Modified Function ---


# Main route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle image generation
@app.route('/generate-art', methods=['POST'])
def generate_art():
    # --- 3. New Key Rotation Logic ---
    global current_key_index
    
    data = request.get_json()
    host = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
    
    params = {
        "prompt": data.get('prompt'),
        "aspect_ratio": data.get('aspect_ratio'),
        "seed": int(data.get('seed', 0)),
        "output_format": data.get('output_format', 'png'),
        "model": "sd3.5-flash",
        "style_preset": data.get('style_preset'),
        "negative_prompt": data.get('negative_prompt'),
        "cfg_scale": float(data.get('cfg_scale', 4.0))
    }
    
    if not params["style_preset"] or params["style_preset"] == "none":
        del params["style_preset"]

    # --- We will try each key, starting from the last known good one ---
    
    # Get a "snapshot" of the current index in a thread-safe way
    with key_lock:
        start_index = current_key_index
    
    num_keys = len(api_keys)
    
    for i in range(num_keys):
        # Calculate which key index to try for this attempt
        index_to_try = (start_index + i) % num_keys
        key_to_use = api_keys[index_to_try]
        
        print(f"Attempt {i+1}/{num_keys} using key index {index_to_try}...")

        try:
            # 1. Send request with the current key
            response = send_generation_request(host, params, key_to_use)
            
            # 2. SUCCESS!
            print(f"Success with key index {index_to_try}.")
            
            # --- Update the global index to this working key ---
            with key_lock:
                current_key_index = index_to_try
            # --- End update ---

            output_image = response.content
            finish_reason = response.headers.get("finish-reason")
            seed = response.headers.get("seed")

            if finish_reason == 'CONTENT_FILTERED':
                return jsonify({'error': 'Generation failed (content filter).'}), 400

            filename = f"gen_{uuid.uuid4().hex[:10]}_{seed}.{params['output_format']}"
            save_path = os.path.join('static', filename)
            
            with open(save_path, "wb") as f:
                f.write(output_image)
            
            return jsonify({
                'image_url': f'/{save_path}',
                'seed': seed
            })

        except Exception as e:
            error_message = str(e).lower()
            print(f"Error with key index {index_to_try}: {error_message}")
            
            # 3. FAILURE. Check why.
            
            # !!--- CRITICAL ERROR CHECK ---!!
            # Check if it's a billing/limit error
            if "lack" in error_message or "credits" in error_message or "purchase" in error_message:
                # This key is dead. Continue the loop to try the next one.
                print(f"Key index {index_to_try} failed due to billing. Trying next key.")
                continue 
            else:
                # This is a *real* error (bad prompt, server down, etc.)
                # We should stop immediately and report it.
                print(f"A non-billing error occurred: {error_message}")
                return jsonify({'error': f"API Error: {error_message}"}), 500
    
    # 4. If we exit the loop, all keys failed the billing check.
    print("All API keys failed billing/limit check.")
    return jsonify({'error': 'All available API keys have reached their billing limit.'}), 500
# --- End of New Logic ---


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)