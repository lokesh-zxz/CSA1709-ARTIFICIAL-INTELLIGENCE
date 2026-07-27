from flask import Flask, request, jsonify, render_template
import torch
import torch.nn as nn
from torchvision import transforms
import numpy as np
import base64
import cv2
import os

app = Flask(__name__)

# Define the model architecture to load state dict
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 47) # 47 classes for EMNIST balanced

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.maxpool(x)
        x = self.relu(self.conv2(x))
        x = self.maxpool(x)
        x = self.relu(self.conv3(x))
        x = x.view(x.size(0), -1) # Flatten
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

MODEL_PATH = 'model.pth'
device = torch.device("cpu") # Inference on CPU is fine
model = CNN()

if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    print("Model loaded successfully.")
else:
    model = None
    print("Warning: model.pth not found. Please run train_model.py first.")

def preprocess_image(image_data):
    """
    Preprocess the base64 encoded image from the canvas to match MNIST format.
    """
    if ',' in image_data:
        image_data = image_data.split(',')[1]
    
    img_bytes = base64.b64decode(image_data)
    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Invert (canvas is white bg, black ink. MNIST is black bg, white digit)
    gray = cv2.bitwise_not(gray)
    
    coords = cv2.findNonZero(gray)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        rect = gray[y:y+h, x:x+w]
        
        size = max(w, h)
        padded = np.zeros((size, size), dtype=np.uint8)
        
        x_offset = (size - w) // 2
        y_offset = (size - h) // 2
        padded[y_offset:y_offset+h, x_offset:x_offset+w] = rect
        
        resized = cv2.resize(padded, (20, 20), interpolation=cv2.INTER_AREA)
        final_img = np.pad(resized, ((4, 4), (4, 4)), 'constant', constant_values=0)
    else:
        final_img = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)
    
    # Convert to PIL Image for torchvision transforms
    from PIL import Image
    pil_img = Image.fromarray(final_img)
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    tensor_img = transform(pil_img).unsqueeze(0) # Add batch dimension
    return tensor_img

@app.route('/')
def index():
    return render_template('index.html')

EMNIST_CLASSES = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'd', 'e', 'f', 'g', 'h', 'n', 'q', 'r', 't'
]

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500
        
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image provided.'}), 400
        
    image_data = data['image']
    
    try:
        processed_img = preprocess_image(image_data)
        
        with torch.no_grad():
            output = model(processed_img)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            predicted_index = torch.argmax(probabilities).item()
            confidence = probabilities[predicted_index].item()
            
            predicted_char = EMNIST_CLASSES[predicted_index]
            
        return jsonify({
            'prediction': predicted_char,
            'confidence': confidence
        })
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
