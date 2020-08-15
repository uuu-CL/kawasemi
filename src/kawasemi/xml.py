"""This module contains several functions which deal with XML files and XML trees.
"""

import os, glob
import xml.etree.ElementTree as ET
import jaconv
from .tokens import Document, Sentence

def create_parsed_xml(xmltree):
    """create a parsed xml.

    under construcion

    """


    
    print('creating parsed xml...')    
    doc = orig_XML_to_doc_obj(xmltree)
    print(len(doc.sentences))
    print(doc.sentences[100].text)





    
    
    
    tree = None    
    return tree

def read_xml(lawID: str) -> ET.ElementTree:
    """Read an XML file for a given lawID.

    This function receives a lawID and returns an XML tree.
    document tree.

    Parameters
    ----------
    lawID : str
      A lawID.

    Returns
    -------
    xml.etree.ElementTree.ElementTree
      An XML tree.

    Examples
    --------

    under construction

"""
    
    xmlbase = lawID + '.xml'

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
        year = lawID[:3]
        xml_glob = os.path.join(os.path.dirname(__file__), 
                                '../../data/orig',
                                year, lawID + '*', lawID + '*.xml')
        
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
    """convert orig to document tree.

    under construction

    """


    
    doc = Document('dummy')
    root = tree.getroot()
    for sent in root.findall('.//Sentence'):
        if sent.text == '' or sent.text == None:
            continue
        text = jaconv.h2z(sent.text, digit=True, ascii=True)        
        doc.sentences.append(Sentence(text))



        




        
    return doc
    
