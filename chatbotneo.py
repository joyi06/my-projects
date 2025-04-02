import requests
import tkinter as tk
from tkinter import scrolledtext

# OpenRouter API Key
API_KEY = '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'
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_openchat_response(user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost:5000",  #website 
        "X-Title": "OpenChat AI"
    }

    payload = {
        "model": "google/gemma-3-27b-it:free",
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 50,
        "temperature": 0.5
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"

def send_message():
    user_message = user_input.get()
    if user_message.strip() == "":
        return

    chat_area.insert(tk.END, f"You: {user_message}\n", "user")
    user_input.delete(0, tk.END)

    bot_response = get_openchat_response(user_message)
    chat_area.insert(tk.END, f"Bot: {bot_response}\n\n", "bot")
    chat_area.see(tk.END)

# GUI Setup
window = tk.Tk()
window.title("OpenChat AI")
window.geometry("500x600")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Helvetica", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("bot", foreground="pink")

user_input = tk.Entry(window, font=("Helvetica", 14))
user_input.pack(padx=10, pady=10, fill=tk.X)

send_button = tk.Button(window, text="send", command=send_message, font=("Helvetica", 12), bg="#4CAF50", fg="black")
send_button.pack(pady=(0, 10))

# Press Enter = Send
window.bind("<Return>", lambda event: send_message())

window.mainloop()