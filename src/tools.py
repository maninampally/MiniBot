def run_calculator(expression):
    try:
        return f"Result: {eval(expression)}"
    except:
        return "Sorry, I couldn't calculate that."

def generate_quiz(topic):
    return f"Here are 3 quiz questions on {topic}:\n1. ...\n2. ...\n3. ..."

def generate_study_plan(topic):
    return f"Here is a 7-day study plan for learning {topic}:\n- Day 1: ...\n- Day 2: ..."

def generate_example(topic):
    if topic == "Python/Pandas":
        return "Example: Load a CSV using Pandas:\n```python\nimport pandas as pd\ndf = pd.read_csv('file.csv')\n```"
    else:
        return "Here is an example related to your topic."
