import os, glob
import xml.etree.ElementTree as ET
import jaconv
from .tokens import Document, Sentence

def create_parsed_xml(xmltree):
    print('creating parsed xml...')    
    doc = orig_XML_to_doc_obj(xmltree)
    print(len(doc.sentences))
    print(doc.sentences[100].text)





    
    
    
    tree = None    
    return tree

def read_xml(lawname, law2Jid, law2id):    
    try:
        lawid = law2id[lawname]
    except KeyError:
        print('You should input a valid law name in Japan.')
        exit()
    xmlbase = lawid + '.xml'

    # Firstly, we search the data/gold/ directory for the xml file.
    xmldir = os.path.join(os.path.dirname(__file__),
                          '../../data/gold')            
    try:
        tree = ET.parse(os.path.join(xmldir, xmlbase))
        print('A gold annotated data used.')
        return tree
    except:
        # Secondly, we search the data/generated/ directory for the xml file.
        xmldir = os.path.join(os.path.dirname(__file__),
                              '../../data/generated')            
    
    try:
        tree = ET.parse(os.path.join(xmldir, xmlbase))
        print('An automatic annotated data used.')
        return tree
    except:        
        # Thirdly, we search the data/orig/ directory for a xml file distributed in e-gov.go.jp.
        year = lawid[:3]
        xml_glob = os.path.join(os.path.dirname(__file__), 
                                '../../data/orig',
                                year, lawid + '*', lawid + '*.xml')
        
    try:
        for filename in glob.glob(xml_glob):            
            orig_tree = ET.parse(filename)
            break
        tree = create_parsed_xml(orig_tree)
        return tree
    except:
        # Finally, we download a xml file from e-gov.go.jp.
        indir = os.path.join(os.path.dirname(__file__), 
                             '../../data/orig')
        url = 'https://elaws.e-gov.go.jp/download/' + year + '.zip'
        
    zipname = download_file(url, indir)
    extract_zip(zipname)
    for filename in glob.glob(xml.glob):            
        orig_tree = ET.parse(filename)
        break
    tree = create_parsed_xml(orig_tree)            
    return tree

def orig_XML_to_doc_obj(tree):
    doc = Document('dummy')
    root = tree.getroot()
    for sent in root.findall('.//Sentence'):
        if sent.text == '' or sent.text == None:
            continue
        text = jaconv.h2z(sent.text, digit=True, ascii=True)        
        doc.sentences.append(Sentence(text))






        
    return doc
    
