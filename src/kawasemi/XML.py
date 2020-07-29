import xml.etree.ElementTree as ET
import jaconv
from .tokens import Document, Sentence

def orig_XML_to_doc_obj(tree):
    doc = Document('dummy')
    root = tree.getroot()
    for sent in root.findall('.//Sentence'):
        if sent.text == '' or sent.text == None:
            continue
        text = jaconv.h2z(sent.text, digit=True, ascii=True)        
        doc.sentences.append(Sentence(text))
    return doc
    
