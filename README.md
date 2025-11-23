# 🤖 MiniBot – Casual Chatbot (DialoGPT)

MiniBot is a lightweight, interactive chatbot built using **Hugging Face Transformers**, **DialoGPT-medium**, and **Gradio**.  
It can carry casual conversations, remember recent chat history, and respond naturally to user inputs.

This project was developed as part of a mini–chatbot assignment using Hugging Face models.

---

## 🚀 Features

### 🗣️ **Casual Conversation**
MiniBot can talk about:
- Daily life  
- Movies  
- Hobbies  
- Fun facts  
- Basic small talk  

### 🧠 **Conversational Memory (Short-Term)**
Uses DialoGPT’s native chat history system (`chat_history_ids`) to maintain context for a few turns.

### 🔐 **Light Safety Filter**
Blocks only extreme unsafe topics to keep conversations friendly and appropriate.

### 💬 **Modern Gradio Interface**
- Chat-style messages
- Clear conversation button
- Clean & responsive UI  
- Works perfectly on **Hugging Face Spaces**

---

## 🏗️ Project Structure

MiniBot/



├── app.py                
├── requirements.txt      
├── README.md             
├── .gitignore               



---

## ⚙️ Tech Stack

| Component | Technology |
|----------|------------|
| **Language Model** | `microsoft/DialoGPT-medium` |
| **Framework** | Hugging Face **Transformers** |
| **UI** | **Gradio 6** |
| **Runtime** | Python (CPU/GPU) |
| **Deployment** | Hugging Face Spaces |

---

## 🧩 How It Works

MiniBot uses the **DialoGPT-medium** model, which is designed for natural open-domain dialogue.  
Each new user message is appended to a running `chat_history_ids` tensor, allowing the model to generate context-aware replies.

Pipeline used:

1. Encode user input  
2. Append to history  
3. Generate new tokens  
4. Decode model output  
5. Return chat-friendly dictionary messages for Gradio  

This results in:
- More natural responses  
- Better short-term memory  
- Smooth back-and-forth conversation  

---

## ▶️ Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/MiniBot
cd MiniBot
```
### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
.venv\Scripts\activate          # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the chatbot
```bash
python app.py
```

Then open: 
```
➡ http://127.0.0.1:7860

