from transformers import AutoModelForCausalLM, AutoTokenizer
from src.config import AppConfig

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(AppConfig.MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(AppConfig.MODEL_NAME)
    return tokenizer, model
