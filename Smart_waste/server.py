# To run this, you first need to install Flask and Flask-CORS:
# pip install Flask Flask-CORS

from flask import Flask, request, jsonify
from flask_cors import CORS

# Import the analysis function from your existing 'app.py' file
# Make sure the file is named 'app.py' or change the import name accordingly.
from app import analyze_waste_image

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing) to allow your frontend
# to communicate with this server.
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    This is the API endpoint that the frontend will call.
    It receives the image data, processes it, and returns the result.
    """
    try:
        # 1. Get the JSON data sent from the frontend
        data = request.get_json()
        if not data or 'imageDataUrl' not in data:
            return jsonify({"error": "Missing imageDataUrl in request"}), 400

        image_data = data['imageDataUrl']

        # 2. Run your existing analysis function from app.py
        result = analyze_waste_image(image_data)

        # 3. Send the result back to the frontend as JSON
        return jsonify(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred on the server."}), 500

# This block allows you to run the server directly from the command line
if __name__ == '__main__':
    # Runs the server on http://127.0.0.1:5000
    # The debug=True flag allows the server to auto-reload when you save changes.
    app.run(host='0.0.0.0', port=5000, debug=True)
