import argparse
import numpy as np
from PIL import Image
import io
import base64
import easyocr
from flask import Flask, request, jsonify

# Initialize EasyOCR Reader
reader = easyocr.Reader(["en"], model_storage_directory="./EasyOCR")

# Initialize Flask app
app = Flask(__name__)

def extract_text_from_image(base64_image):
  try:
    # Convert the base64 image to bytes
    image_bytes = base64.b64decode(base64_image[22:])
    # Create a BytesIO object from the image bytes
    image_buffer = io.BytesIO(image_bytes)
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(image_buffer)
    # Convert the image to grayscale (optional but can improve OCR accuracy)
    image = image.convert("L")

    # Convert PIL image to OpenCV format
    open_cv_image = np.array(image)

    result = reader.readtext(open_cv_image, detail=0)
    if result:
      return result[0].replace(" ", "")
    else:
      return "ABCDEF"
  except Exception as e:
    return f"Error processing image: {str(e)}"

@app.route("/extract-text", methods=["POST"])
def extract_text():
  # Get the base64 image from the request
  data = request.get_json()
  base64_image = data.get("image", "")

  if not base64_image:
    return jsonify({"error": "No base64 image string provided"}), 400

  extracted_text = extract_text_from_image(base64_image)
  return jsonify({"extracted_text": extracted_text})

@app.route('/')
def health_check():
  return "Server is running", 200

if __name__ == "__main__":
  # Run Flask server
  app.run(host="0.0.0.0", port=5000)
