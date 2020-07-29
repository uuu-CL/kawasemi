import os, glob
import csv
import xml.etree.ElementTree as ET
import unicodedata
import re
from . import models
from .download import download_file, extract_zip
from .XML import orig_XML_to_doc_obj

def kansuji_to_num(x):
    result = 0
    nums = [int(unicodedata.numeric(l)) for l in x[:]]
    nums2 = [nums.pop(0)]
    
    for n in nums:
        if n < 10:
            nums2.append(n)
        else:
            nums2[-1] *= n
    for n in nums2:
        result += n

    return result
    
def Jid_to_id(x):
    '''Convert a string such as  '明治二十九年法律第八十九号' to the id such as '129AC0000000089'
'''
    era2id = {'明治': 1, '大正': 2, '昭和': 3, '平成': 4, '令和': 5}
    lawtype2id = {'法律': 'AC'}
    
    m = re.match(r'(.{2})(.+)年(.+)第(.+)号', x)
    era = era2id[m.group(1)]
    year = kansuji_to_num(m.group(2).replace('元', '一'))
    lawtype = lawtype2id[m.group(3)]
    num = kansuji_to_num(m.group(4))

    return '{:3d}{:s}{:010d}'.format(era * 100 + year, lawtype, num)    

def read_abbr(filename=None):
    if filename == None:
        filename = os.path.join(os.path.dirname(__file__),
                                '../../data/utils/abbr.tsv')     
    law2Jid = {}
    law2id = {}
    
    with open(filename, 'r') as f:
        for line in csv.reader(f, delimiter='\t'):
            law2Jid[line[0]] = line[1]
            law2id[line[0]] = Jid_to_id(line[1])
    return law2Jid, law2id

def create_parsed_xml(xmltree):
    print('creating parsed xml...')    
    doc = orig_XML_to_doc_obj(xmltree)
    print(len(doc.sentences))
    print(doc.sentences[100].text)


    
    
    tree = None    
    return tree


def read_xml(lawname):
    # law name to law ID in Japanese, law name to law ID
    law2Jid, law2id = read_abbr()    

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
    
def load_model(lawname):
    tree = read_xml(lawname)
    return models.Statute(lawname)

