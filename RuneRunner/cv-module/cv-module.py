from flask import Flask, request, jsonify
from cv_analysis import CVAnalysis
import base64
import io
from PIL import Image

app = Flask(__name__)
cv_model = CVAnalysis()

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    img = Image.open(image.stream)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    result = cv_model.analyze_image(img_byte_arr)
    return jsonify({'analysis': result})

@app.route('/detect_text', methods=['POST'])
def detect_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    img = Image.open(image.stream)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    text = cv_model.detect_text(img_byte_arr)
    return jsonify({'detected_text': text})

@app.route('/analyze_social_media', methods=['POST'])
def analyze_social_media():
    data = request.json
    analysis = "Sample social media analysis"  # Platzhalter
    return jsonify({'analysis': analysis})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
