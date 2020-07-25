
class NLP():
    def __init__(self, text):
        self.mrph = []
        self.text = text
        
    def show(self):
        print(self.text)

def load(filename):
    return NLP(filename)

