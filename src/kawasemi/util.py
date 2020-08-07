import os
import csv
import unicodedata
import re
from . import models
from .download import download_file, extract_zip
from .xml import read_xml, orig_XML_to_doc_obj

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
    '''Convert 

    a string such as  '明治二十九年法律第八十九号' to the id such as '129AC0000000089'

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.
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
    
def load_model(lawname):
    law2Jid, law2id = read_abbr()
    tree = read_xml(lawname, law2Jid, law2id)
    return models.Statute(lawname)

