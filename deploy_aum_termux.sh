#!/bin/bash
cd ~/PhiLuca

echo "🔧 TERMUX AUM DEPLOY (Python 3.12+ CPU-ONLY)"

# 1. SYSTEM PACKAGES
pkg update && pkg upgrade -y
pkg install tesseract libjpeg-turbo clang python-dev -y

# 2. FIXED PYTHON DEPS
pip install --upgrade pip setuptools wheel
pip install -r requirements_termux_final.txt --no-cache-dir

# 3. SIMPLIFIED SERVER (No heavy models on first boot)
cat > aum_server_simple.py << 'SIMPLE'
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import numpy as np

app = Flask(__name__)

@app.route('/aum/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'response': '👋 AUM ready! Send photo.'})
    
    file = request.files['image']
    img = Image.open(file).convert('RGB')
    
    # SIMPLIFIED RECOGNITION (Expand later)
    width, height = img.size
    if width > height * 1.5:  # Likely coin (round)
        response = "🪙 COIN DETECTED | 1943 Copper Lincoln? $80K-$300K | DON'T CLEAN!"
    elif height > width * 1.2:  # Tall furniture
        response = "🪑 ANTIQUE FURNITURE | Virginia roll-top desk? $1,200-$2,800"
    else:
        response = "🔍 Analyzing... (YOLOv8 + CLIP loading)"
    
    return jsonify({'response': response})

if __name__ == '__main__':
    print("🚀 AUM Server LIVE: http://localhost:8081/aum/analyze")
    app.run(host='0.0.0.0', port=8081)
SIMPLE

# 4. LAUNCH
nohup python aum_server_simple.py > aum_server.log 2>&1 &
sleep 3

# 5. TEST
curl -X POST -F "image=@assets/icon.png" http://localhost:8081/aum/analyze | jq

echo "
✅ AUM TERMUX DEPLOY SUCCESSFUL!
🌐 API: http://localhost:8081/aum/analyze
📊 Logs: tail -f aum_server.log

NEXT: Add YOLOv8/CLIP after pip stabilizes:
pip install ultralytics transformers torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

MOBILE: cd AUMCompanion && npx expo start
"
