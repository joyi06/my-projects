from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Carica il modello pre-addestrato
model_name = "microsoft/DialoGPT-small"
print("🔄 Caricamento modello...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
print("✅ Modello caricato!")

# Inizio conversazione
chat_history_ids = None
print("\n🤖 Chatbot attivo! Scrivi 'esci' per terminare.\n")

while True:
    # Input dell'utente
    user_input = input("Tu: ")
    if user_input.lower() == "esci":
        print("Chatbot: Ciao! Alla prossima 👋")
        break

    # Codifica l'input
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

    # Aggiungi lo storico della chat se presente
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    # Genera la risposta
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.9
    )

    # Decodifica e stampa la risposta
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    print("Chatbot:", bot_response)