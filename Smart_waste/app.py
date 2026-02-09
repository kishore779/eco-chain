import time
import base64
import io
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

# Load pre-trained model once (MobileNetV2)
model = MobileNetV2(weights='imagenet')

# Define custom waste categories (example mapping)
waste_categories = ['Plastic Bottles', 'Organic/Food', 'Hazardous Chemical', 'Construction Debris', 'Mixed General']

def analyze_waste_image(image_data_url: str):
    """
    Uses a real AI model (MobileNetV2) to analyze the image and classify waste.
    """
    print("Analyzing image using AI model...")

    # 1. Simulate processing delay
    time.sleep(1.0)

    # 2. Extract base64 image data and decode it
    image_base64 = image_data_url.split(",")[1]  # Remove data:image/jpeg;base64,
    image_bytes = base64.b64decode(image_base64)

    # 3. Open the image and resize to model's expected size (224x224 for MobileNetV2)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    # 4. Convert to numpy array and preprocess
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # 5. Predict using MobileNetV2
    preds = model.predict(img_array)
    decoded = decode_predictions(preds, top=1)[0][0]  # (class_id, label, confidence)

    # Extract top prediction details
    predicted_label = decoded[1]
    confidence_score = float(decoded[2])

    # 6. Map to our waste categories (simplified mapping example)
    # You can improve this mapping or train a custom model on waste data
    if 'bottle' in predicted_label.lower():
        waste_type = 'Plastic Bottles'
    elif 'banana' in predicted_label.lower() or 'apple' in predicted_label.lower():
        waste_type = 'Organic/Food'
    elif 'chemical' in predicted_label.lower() or 'cleanser' in predicted_label.lower():
        waste_type = 'Hazardous Chemical'
    elif 'wall' in predicted_label.lower() or 'stone' in predicted_label.lower():
        waste_type = 'Construction Debris'
    else:
        waste_type = 'Mixed General'

    # 7. Determine severity based on confidence
    if confidence_score > 0.85:
        severity = 'Critical'
    elif confidence_score > 0.65:
        severity = 'High'
    elif confidence_score > 0.4:
        severity = 'Medium'
    else:
        severity = 'Low'

    # 8. Assemble final result
    analysis_result = {
        'severity': severity,
        'wasteType': waste_type,
        'confidence': round(confidence_score, 2),
        'modelPrediction': predicted_label
    }

    print("AI Analysis Complete.")
    return analysis_result

# --- Example usage ---
if __name__ == "__main__":
    # Load a sample image from file (replace with your base64 data in real app)
    with open("sample_image.jpg", "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
    image_data_url = "data:image/jpeg;base64," + base64_image

    result = analyze_waste_image(image_data_url)
    print("\n--- AI ANALYSIS RESULT ---")
    print(f"Severity:   {result['severity']}")
    print(f"Waste Type: {result['wasteType']}")
    print(f"Confidence: {result['confidence'] * 100:.0f}%")
    print(f"Model Pred: {result['modelPrediction']}")
