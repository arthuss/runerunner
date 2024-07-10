import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM
import numpy as np

class CentralLLM:
    def __init__(self):
        # Lade Modelle und Tokenizer
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        
        self.gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.gpt_model = AutoModelForCausalLM.from_pretrained("gpt2")

    def analyze_market_data(self, market_data):
        # Implementiere hier die Logik zur Analyse von Marktdaten
        analysis = f"Analyzed market data: {market_data[:100]}..."  # Beispielimplementierung
        return analysis

    def adjust_strategy(self, current_strategy, performance_metrics):
        # Implementiere hier die Logik zur Anpassung der Strategie
        adjusted_strategy = f"Adjusted strategy based on: {performance_metrics}"  # Beispielimplementierung
        return adjusted_strategy

    def analyze_sentiment(self, text):
        inputs = self.sentiment_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.sentiment_model(**inputs)
        sentiment_score = torch.softmax(outputs.logits, dim=1).tolist()[0][1]
        
        if sentiment_score > 0.6:
            return "Positive"
        elif sentiment_score < 0.4:
            return "Negative"
        else:
            return "Neutral"

    def generate_report(self, report_type, data):
        prompt = f"Generate a {report_type} report based on the following data:\n{data}\n\nReport:"
        inputs = self.gpt_tokenizer(prompt, return_tensors="pt")
        outputs = self.gpt_model.generate(**inputs, max_length=500, num_return_sequences=1)
        report = self.gpt_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return report
