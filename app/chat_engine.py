from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from app.config import MAX_MODEL_INPUT_LENGTH

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GPT2LMHeadModel.from_pretrained("distilgpt2").to(device)
tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")

def chat_completion(prompt, max_length=150):
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=MAX_MODEL_INPUT_LENGTH - max_length).to(device)
    outputs = model.generate(inputs, max_length=inputs.shape[1]+max_length, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("Assistant:")[-1].strip()
 
