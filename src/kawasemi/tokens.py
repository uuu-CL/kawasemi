from pyknp import Juman, KNP

class JNLP(object):
    '''Japanese parser class.
    '''
    def __init__(self):
        '''initialize

        Args:
          Nothing

        Returns:
          Nothing

        Examples:
          nlp = JNLP()
        '''
        
        self.juman = Juman()
        self.KNP = KNP(option='-tab -anaphora')
        
    def POStagger(self, text):
        '''annotate a input text with POS tags.

        Args:
          text (str): a text which should be tokenized

        Returns:
          mrphs (List[str]): a list of tokens

        Examples:
          a = nlp.POStagger('この文を解析します。')
        '''
        
        result = self.juman.analysis(text)
        mrphs = [mrph.midasi for mrph in result.mrph_list()]
        return mrphs

    def parse(self, text):
        result = self.knp.parse(text)
        for bnst in result.bnst_list():
            print(bnst.bnst_id, bnst.dpndtype, bnst.parent_id, bnst.fstring)
            print(' '.join([mrph.midasi for mrph in bnst.mrph_list()]))
        for tag in result.tag_list():
            print(tag.tag_id, tag.dpndtype, tag.parent_id, tag.fstring)
            print(' '.join([mrph.midasi for mrph in tag.mrph_list()]))
            if tag.pas != None:
                for key in tag.pas.arguments:
                    arg = tag.pas.arguments[key][0]
                    print(key)
                    print(arg.tid, arg.eid, arg.midasi, arg.flag)
        return result

class Event(object):
    def __init__(self, text):
        self.core = text
        self.arguments = []
        
    def __str__(self):
        return self.core
    
class Token(object):
    def __init__(self, text):
        self.text = text
        self.neg_exp = None # 否定語かどうか
        
    def __str__(self):
        return self.text

class BNST(object):
    def __init__(self, text):
        self.text = text
        self.tokens = []
        
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

class Article(object):
    def __init__(self, text, aid):
        self.id = aid
        self.text = text
        self.tokens = []
        self.sentences = []
        self.paragraphs = []

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
        
class Statute(Document):
    def __init__(self, text):
        super().__init__(text)
        self.articles = []

    def __str__(self):
        return self.text    
        
