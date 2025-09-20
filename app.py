from flask import Flask, request, jsonify, render_template_string
import joblib
import re
import string
import os

app = Flask(__name__)

# Load the trained model and vectorizer
try:
    model = joblib.load('imdb_logreg_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
    print("✅ Model and vectorizer loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    tfidf = None

def clean_text(text):
    """Clean and preprocess text data"""
    text = text.lower()  # lowercase
    text = re.sub(r"<.*?>", "", text)  # remove HTML tags
    text = re.sub(r"\d+", "", text)  # remove numbers
    text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    return text

@app.route('/')
def home():
    """Home page with a simple interface"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>IMDB Sentiment Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
            textarea { width: 100%; height: 150px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
            .positive { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .negative { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 IMDB Movie Review Sentiment Analysis</h1>
            <p>Enter a movie review below to analyze its sentiment:</p>
            <form id="sentimentForm">
                <textarea id="review" placeholder="Enter your movie review here..." required></textarea><br><br>
                <button type="submit">Analyze Sentiment</button>
            </form>
            <div id="result"></div>
        </div>
        
        <script>
            document.getElementById('sentimentForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const review = document.getElementById('review').value;
                const resultDiv = document.getElementById('result');
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({review: review})
                    });
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        resultDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
                    } else {
                        const sentiment = data.prediction;
                        const confidence = data.confidence;
                        const sentimentClass = sentiment === 'positive' ? 'positive' : 'negative';
                        const emoji = sentiment === 'positive' ? '😊' : '😞';
                        
                        resultDiv.innerHTML = `
                            <div class="result ${sentimentClass}">
                                <h3>${emoji} Sentiment: ${sentiment.toUpperCase()}</h3>
                                <p>Confidence: ${(confidence * 100).toFixed(2)}%</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">Error: ${error.message}</div>`;
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for sentiment prediction"""
    try:
        if model is None or tfidf is None:
            return jsonify({'error': 'Model not loaded properly'}), 500
            
        data = request.get_json()
        if not data or 'review' not in data:
            return jsonify({'error': 'No review text provided'}), 400
            
        # Clean and preprocess the text
        cleaned_text = clean_text(data['review'])
        
        # Transform the text using TF-IDF
        text_tfidf = tfidf.transform([cleaned_text])
        
        # Make prediction
        prediction = model.predict(text_tfidf)[0]
        confidence = model.predict_proba(text_tfidf)[0].max()
        
        # Convert prediction to sentiment label
        sentiment = 'positive' if prediction == 1 else 'negative'
        
        return jsonify({
            'prediction': sentiment,
            'confidence': float(confidence),
            'original_text': data['review']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'vectorizer_loaded': tfidf is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
