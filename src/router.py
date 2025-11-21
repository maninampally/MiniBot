from src.prompts import build_persona_prompt
from src.tools import run_calculator, generate_quiz, generate_study_plan, generate_example
from src.config import AppConfig
import torch

def handle_message(user_message, history, persona, topic, level, tokenizer, model, analytics):

    # Tool routing
    if user_message.startswith("calc:"):
        expr = user_message.replace("calc:", "").strip()
        reply = run_calculator(expr)
        history.append((user_message, reply))
        return reply, history
    
    if user_message.startswith("quiz:"):
        q_topic = user_message.replace("quiz:", "").strip()
        reply = generate_quiz(q_topic)
        history.append((user_message, reply))
        return reply, history

    if user_message.startswith("plan:"):
        plan_topic = user_message.replace("plan:", "").strip()
        reply = generate_study_plan(plan_topic)
        history.append((user_message, reply))
        return reply, history
    
    if user_message.startswith("example:"):
        topic = user_message.replace("example:", "").strip()
        reply = generate_example(topic)
        history.append((user_message, reply))
        return reply, history

    # Build persona prompt
    persona_prompt = build_persona_prompt(persona, topic, level)

    # Build context
    context = ""
    for turn in history[-AppConfig.MAX_HISTORY_TURNS:]:
        context += f"User: {turn[0]}\nBot: {turn[1]}\n"

    final_input = persona_prompt + context + f"User: {user_message}\nBot:"

    inputs = tokenizer.encode(final_input, return_tensors="pt")
    outputs = model.generate(inputs, max_length=inputs.shape[1] + AppConfig.MAX_TOKENS, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True).split("Bot:")[-1]

    # Update analytics
    analytics.update(persona, topic)

    # Update history
    history.append((user_message, reply))

    return reply, history
