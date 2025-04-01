# llm_model.py
from transformers import BertForSequenceClassification, BertTokenizer
import torch

class LLMScorer:
    def __init__(self, model_name="textattack/bert-base-uncased-imdb"):
        # Using a pre-trained BERT model
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertForSequenceClassification.from_pretrained(model_name)

    def score_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.logits[0][1].item()

    def get_best_text(self, words):
        if not words:
            return None, None

        scores = {word: self.score_text(word) for word in words}
        best_text = max(scores, key=scores.get) 
        return best_text, scores

