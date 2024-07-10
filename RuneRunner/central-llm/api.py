from flask import Flask, request, jsonify
from central_llm import CentralLLM
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
llm = CentralLLM()

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Konfiguriere Rate Limiting
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze():
    data = request.json
    if 'market_data' not in data:
        return jsonify({'error': 'No market data provided'}), 400
    try:
        analysis = llm.analyze_market_data(data['market_data'])
        logger.info(f"Analysis performed for market data")
        return jsonify({'analysis': analysis})
    except Exception as e:
        logger.error(f"Error during market data analysis: {str(e)}")
        return jsonify({'error': 'An error occurred during analysis'}), 500

@app.route('/adjust-strategy', methods=['POST'])
@limiter.limit("5 per minute")
def adjust_strategy():
    data = request.json
    if 'current_strategy' not in data or 'performance_metrics' not in data:
        return jsonify({'error': 'Missing required data'}), 400
    try:
        adjusted_strategy = llm.adjust_strategy(data['current_strategy'], data['performance_metrics'])
        logger.info(f"Strategy adjusted based on performance metrics")
        return jsonify({'adjusted_strategy': adjusted_strategy})
    except Exception as e:
        logger.error(f"Error during strategy adjustment: {str(e)}")
        return jsonify({'error': 'An error occurred during strategy adjustment'}), 500

@app.route('/sentiment-analysis', methods=['POST'])
@limiter.limit("20 per minute")
def sentiment_analysis():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided for sentiment analysis'}), 400
    try:
        sentiment = llm.analyze_sentiment(data['text'])
        logger.info(f"Sentiment analysis performed")
        return jsonify({'sentiment': sentiment})
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {str(e)}")
        return jsonify({'error': 'An error occurred during sentiment analysis'}), 500

@app.route('/generate-report', methods=['POST'])
@limiter.limit("2 per minute")
def generate_report():
    data = request.json
    if 'report_type' not in data or 'data' not in data:
        return jsonify({'error': 'Missing required data for report generation'}), 400
    try:
        report = llm.generate_report(data['report_type'], data['data'])
        logger.info(f"Report generated: {data['report_type']}")
        return jsonify({'report': report})
    except Exception as e:
        logger.error(f"Error during report generation: {str(e)}")
        return jsonify({'error': 'An error occurred during report generation'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'central-llm'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
