import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

# OpenRouter API Key - REPLACE WITH YOUR ACTUAL KEY
API_KEY = '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'  
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Conversation history with system message
conversation_history = [
    {
        "role": "system", 
        "content": f"You are a helpful AI assistant. Today is {datetime.now().strftime('%B %d, %Y')}."
    }
]

def get_openchat_response(user_message):
    global conversation_history

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",  # Required by OpenRouter
        "X-Title": "My AI App",              # Required by OpenRouter
        "Content-Type": "application/json"
    }

    conversation_history.append({"role": "user", "content": user_message})
    conversation_history = conversation_history[-10:]  # Keep last 10 messages

    payload = {
        "model": "google/gemma-3-27b-it:free",
        "messages": conversation_history,
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        
        bot_message = response.json()["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": bot_message})
        return bot_message
        
    except requests.exceptions.HTTPError as err:
        return f"HTTP Error: {err}"
    except Exception as e:
        return f"Error: {str(e)}"

def send_message():
    user_message = user_input.get().strip()
    if not user_message:
        return

    chat_area.insert(tk.END, f"You: {user_message}\n", "user")
    user_input.delete(0, tk.END)
    
    # Disable send button during request
    send_button.config(state=tk.DISABLED)
    window.update()
    
    try:
        bot_response = get_openchat_response(user_message)
        chat_area.insert(tk.END, f"Bot: {bot_response}\n\n", "bot")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get response: {e}")
    
    chat_area.see(tk.END)
    send_button.config(state=tk.NORMAL)

# GUI Setup
window = tk.Tk()
window.title("AI Assistant")
window.geometry("600x700")

# Chat area
chat_area = scrolledtext.ScrolledText(
    window, 
    wrap=tk.WORD, 
    font=("Arial", 12),
    padx=10,
    pady=10
)
chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("bot", foreground="green")

# Input area
input_frame = tk.Frame(window)
input_frame.pack(fill=tk.X, padx=10, pady=10)

user_input = tk.Entry(
    input_frame, 
    font=("Arial", 14)
   ) 
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    font=("Arial", 13),
    bg="#4CAF50",
    fg="blue"
)
send_button.pack(side=tk.RIGHT, padx=(10, 0))

window.bind("<Return>", lambda event: send_message())

window.mainloop()