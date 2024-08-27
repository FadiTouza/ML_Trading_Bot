"""
This module provides functionality to estimate the sentiment of news articles using the FinBERT model.
It leverages the Hugging Face transformers library to tokenize input text and perform sequence classification
to determine whether the sentiment is positive, negative, or neutral.
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Determine the device to run the model on (GPU if available, else CPU)
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load the tokenizer for the FinBERT model.
# Consider manually loading the model for added safety due to weights_only=False being default in PyTorch.
# Check if weights_only=True becomes the default in torch.load method in future updates (current version == 2.4.0).
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]


def get_sentiment(news):
    """
    Estimates the sentiment of given news articles.

    Args:
        news (list of str): The news articles to analyze.

    Returns:
        tuple:
            float: The probability of the predicted sentiment.
            str: The sentiment label ("positive", "negative", or "neutral").
    """
    if news:
        # Tokenize the news articles
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        # Get the sentiment logits from FinBERT
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]
        # Apply softmax to obtain probabilities
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)

        # Determine the highest probability sentiment
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        # Return neutral sentiment with zero probability if no news is provided
        return 0, labels[-1]


if __name__ == "__main__":
    """
    Example usage of the get_sentiment function.
    """
    tensor, sentiment = get_sentiment(['Top companies show bad performance on quarterly report.'])
    print(tensor, sentiment)
