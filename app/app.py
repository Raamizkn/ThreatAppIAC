import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple in-memory model for threat detection
# In a real application, this would be a more sophisticated model
class ThreatDetector:
    def __init__(self):
        # Initialize with some example data
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        
        # Example training data
        example_emails = [
            "Hello, how are you doing today?",
            "Meeting scheduled for tomorrow at 2pm",
            "Please find attached the report",
            "URGENT: Your account has been compromised",
            "Click here to claim your prize",
            "Your password needs to be reset immediately",
            "Transfer funds to this account number",
            "You've won a lottery ticket",
            "Confidential: Wire transfer needed"
        ]
        
        labels = [0, 0, 0, 1, 1, 1, 1, 1, 1]  # 0: safe, 1: threat
        
        # Train the model
        X = self.vectorizer.fit_transform(example_emails)
        self.classifier.fit(X, labels)
        logger.info("Threat detection model initialized")
    
    def predict(self, text):
        """Predict if the given text is a threat"""
        try:
            X = self.vectorizer.transform([text])
            prediction = self.classifier.predict(X)[0]
            probability = self.classifier.predict_proba(X)[0][prediction]
            return {
                'is_threat': bool(prediction),
                'confidence': float(probability),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return {
                'error': str(e),
                'is_threat': False,
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat()
            }

# Initialize the threat detector
threat_detector = ThreatDetector()

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/detect', methods=['POST'])
def detect_threat():
    """API endpoint to detect threats in the provided text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            logger.warning("Invalid request: missing 'text' field")
            return jsonify({'error': "Missing 'text' field"}), 400
        
        text = data['text']
        logger.info(f"Processing text: {text[:50]}...")
        
        result = threat_detector.predict(text)
        
        # Log the result
        threat_status = "THREAT" if result['is_threat'] else "SAFE"
        logger.info(f"Detection result: {threat_status} with confidence {result['confidence']:.2f}")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-detect', methods=['POST'])
def batch_detect():
    """API endpoint to detect threats in multiple texts"""
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data or not isinstance(data['texts'], list):
            logger.warning("Invalid request: missing or invalid 'texts' field")
            return jsonify({'error': "Missing or invalid 'texts' field"}), 400
        
        texts = data['texts']
        logger.info(f"Processing batch of {len(texts)} texts")
        
        results = []
        for text in texts:
            result = threat_detector.predict(text)
            results.append(result)
        
        return jsonify({'results': results})
    
    except Exception as e:
        logger.error(f"Error processing batch request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true') 