from transformers import BertForSequenceClassification, BertTokenizer
import torch

# Escolha o nome do modelo que você deseja usar
model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'

# Carregar o tokenizer e o modelo
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Certifique-se de que o modelo está na CPU (ou mude para .cuda() se tiver GPU)
device = torch.device("cpu")
model = model.to(device)

# Texto de exemplo para classificação
text = "I love this product! It works great."

# Tokenizando o texto
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

# Movendo os tensores para o mesmo dispositivo do modelo
inputs = {key: value.to(device) for key, value in inputs.items()}

# Colocando o modelo em modo de avaliação
model.eval()

# Inferência sem calcular gradientes
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)

# O resultado está em 'predictions', que você pode mapear de volta para rótulos reais se necessário
print("Classificação do Sentimento:", predictions.item())