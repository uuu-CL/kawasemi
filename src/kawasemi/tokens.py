class Token(object):
    def __init__(self, text):
        self.text = text
        
    def __str__(self):
        return self.text

class Sentence(object):
    def __init__(self, text):
        self.text = text
        self.tokens = []
        
    def __str__(self):
        return self.text    

class Paragraph(object):
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.sentences = []

    def __str__(self):
        return self.text    

class Document(object):
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.sentences = []
        self.paragraphs = []

    def __str__(self):
        return self.text    
        
