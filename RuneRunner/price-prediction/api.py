from flask import Flask, request, jsonify
from central_llm import CentralLLM

app = Flask(__name__)
llm = CentralLLM()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    analysis = llm.analyze_market_data(data['market_data'])
    return jsonify({'analysis': analysis})

@app.route('/adjust-strategy', methods=['POST'])
def adjust_strategy():
    data = request.json
    adjusted_strategy = llm.adjust_strategy(data['current_strategy'], data['performance_metrics'])
    return jsonify({'adjusted_strategy': adjusted_strategy})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
