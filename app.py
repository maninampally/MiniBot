import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "microsoft/DialoGPT-medium"

print("===== Application Startup =====")
print("Loading model and tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print("Device:", device)
print("Model loaded.")

# ---------------------------------------------------------
# LIGHT SAFETY FILTER 
# ---------------------------------------------------------

BLOCK_KEYWORDS = [
    "nsfw", "sex", "porn", "murder", "kill", "suicide", "self-harm"
]

def is_strongly_unsafe(text: str) -> bool:
    """Very small filter — only block MAJOR issues."""
    txt = text.lower()
    return any(word in txt for word in BLOCK_KEYWORDS)


# ---------------------------------------------------------
# NORMAL CHATBOT BEHAVIOR (DialoGPT-Style)
# ---------------------------------------------------------

def build_prompt(messages, new_user_text):
    """
    Only light steering.
    Pure conversation history:
    User: ...
    Bot: ...
    """
    prompt = ""

    # last 6 turns
    history = messages[-6:] if messages else []

    for m in history:
        role = m.get("role")
        content = m.get("content")
        if role == "user":
            prompt += f"User: {content}\n"
        else:
            prompt += f"Bot: {content}\n"

    # new message
    prompt += f"User: {new_user_text}\nBot:"

    return prompt


def generate_reply(messages, user_input):
    # Hard block only severe unsafe inputs
    if is_strongly_unsafe(user_input):
        return (
            "I’m here to keep our chat positive and safe 😊 "
            "Let’s talk about hobbies, movies, food, travel, or anything fun!"
        )

    prompt = build_prompt(messages, user_input)

    enc = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    output_ids = model.generate(
        **enc,
        max_new_tokens=60,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,       # IMPORTANT — DialoGPT needs sampling
        top_p=0.95,
        top_k=50,
        temperature=0.8       # makes responses fun & stable
    )

    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Extract only bot's last turn
    if "Bot:" in decoded:
        reply = decoded.split("Bot:")[-1].strip()
    else:
        reply = decoded.strip()

    # Remove weird DialoGPT glitches
    if len(reply) < 1:
        reply = "Haha! That's interesting 😄"
    if len(reply) > 200:
        reply = reply[:200]

    # Soft safety check on model output
    if is_strongly_unsafe(reply):
        reply = (
            "Let’s keep things friendly and chill 😄 "
            "Tell me something fun or ask anything casual!"
        )

    return reply


# ---------------------------------------------------------
# GRADIO CHATBOT
# ---------------------------------------------------------

WELCOME_MESSAGE = {
    "role": "assistant",
    "content": "Hey! I'm MiniBot 🤖. Let's chat! Tell me anything casual 😄"
}

def respond(user_message, messages):
    if messages is None or len(messages) == 0:
        messages = [WELCOME_MESSAGE]

    user_message = user_message.strip()

    # Add user message
    messages = messages + [{"role": "user", "content": user_message}]

    # Generate reply
    reply = generate_reply(messages, user_message)

    # Add bot reply
    messages = messages + [{"role": "assistant", "content": reply}]

    return messages, ""


def clear_chat():
    return [WELCOME_MESSAGE], ""


# ---------------------------------------------------------
# UI
# ---------------------------------------------------------

with gr.Blocks(title="MiniBot – Chill Chatbot") as demo:
    gr.Markdown("## 🤖 MiniBot – Friendly Chill Chatbot")
    gr.Markdown(
        "MiniBot is here to chat casually! 😊\n"
        "Talk about movies, hobbies, travel, food, music — anything fun and safe!"
    )

    chatbot = gr.Chatbot(value=[WELCOME_MESSAGE])
    msg = gr.Textbox(placeholder="Say something fun! 😊")
    clear = gr.Button("🧹 Clear Chat")

    msg.submit(respond, [msg, chatbot], [chatbot, msg])
    clear.click(clear_chat, None, [chatbot, msg], queue=False)

if __name__ == "__main__":
    demo.launch()
