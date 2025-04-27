from flask import Flask, request, jsonify
from predictor import predict_exam_score, suggest_improvements
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import os
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configuration
API_KEYS = {
    os.getenv('FRONTEND_API_KEY'): "frontend-client"  # Store keys in environment variables
}

# API Key Decorator
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        if api_key in API_KEYS:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Invalid or missing API key"}), 401
    return decorated_function

    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        student_data = request.json
        desired_score = float(student_data.pop('desired_score', 90)) if student_data else 90
        predicted_score = predict_exam_score(student_data)
        suggestions = suggest_improvements(student_data, predicted_score, desired_score)
        return jsonify({
            'predicted_score': round(float(predicted_score), 2),
            'desired_score': desired_score,
            'score_gap': desired_score - predicted_score,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)