class Analytics:
    def __init__(self):
        self.total_messages = 0
        self.topic_usage = {}
        self.persona_usage = {}

    def update(self, persona, topic):
        self.total_messages += 1

        if topic not in self.topic_usage:
            self.topic_usage[topic] = 0
        self.topic_usage[topic] += 1

        if persona not in self.persona_usage:
            self.persona_usage[persona] = 0
        self.persona_usage[persona] += 1
