def build_persona_prompt(persona, topic, level):
    base = f"You are a helpful Data Science tutor specializing in {topic} at a {level} level.\n"

    if persona == "Stats Tutor":
        persona_txt = "Explain statistics concepts simply, using examples."
    elif persona == "Python & Pandas Helper":
        persona_txt = "Help with Python basics, Pandas operations, and code examples."
    elif persona == "ML Concepts Coach":
        persona_txt = "Explain machine learning concepts clearly with analogies."
    elif persona == "Project Mentor":
        persona_txt = "Provide guidance on data science project structure and workflow."
    else:
        persona_txt = "Provide general helpful responses."

    return base + persona_txt + "\n\n"
