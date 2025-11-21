import gradio as gr
from src.model_loader import load_model
from src.router import handle_message
from src.analytics import Analytics
from src.config import AppConfig

# Load model and tokenizer
tokenizer, model = load_model()

# Initialize analytics tracker
analytics = Analytics()

def chat_interface(user_message, history, persona, topic, level):
    response, history_updated = handle_message(
        user_message=user_message,
        history=history,
        persona=persona,
        topic=topic,
        level=level,
        tokenizer=tokenizer,
        model=model,
        analytics=analytics
    )
    return history_updated

# ------------------------
# UI components
# ------------------------
personas = ["Stats Tutor", "Python & Pandas Helper", "ML Concepts Coach", "Project Mentor"]
topics = ["Statistics", "Python/Pandas", "Machine Learning", "Data Science Projects"]
levels = ["Beginner", "Intermediate"]

with gr.Blocks(title="DataSensei – Data Science Learning Assistant 🤖📊") as demo:
    
    gr.Markdown("# **DataSensei – Data Science Learning Assistant 🤖📊**")
    gr.Markdown("Ask me anything about Python, Pandas, Stats, or Machine Learning!")

    with gr.Row():
        persona_dd = gr.Dropdown(label="Persona", choices=personas, value="Python & Pandas Helper")
        topic_dd = gr.Dropdown(label="Topic", choices=topics, value="Python/Pandas")
        level_dd = gr.Dropdown(label="Level", choices=levels, value="Beginner")

    chatbot = gr.Chatbot(height=450)

    with gr.Row():
        msg_box = gr.Textbox(label="Ask a question")
        clear_btn = gr.Button("Clear Chat")

    def start_chat(msg, history):
        return "", history

    msg_box.submit(chat_interface, [msg_box, chatbot, persona_dd, topic_dd, level_dd], chatbot)
    clear_btn.click(lambda: None, None, chatbot, queue=False)

demo.launch()
