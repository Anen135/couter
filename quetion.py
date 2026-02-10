class Quetion:
    def __init__(self, text, answers, current_answer):
        self.text = text
        self.answers = answers
        self.current_answer = current_answer

    def check_answer(self, answer):
        return self.current_answer == answer

    def __str__(self):
        return f"Question: {self.text}\nAnswers: {', '.join(self.answers)}"