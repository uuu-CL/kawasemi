"""This module contains utility functions which other modules use.
"""

import os
import csv
import unicodedata
import re
from . import models
from .download import download_file, extract_zip
from .xml import read_xml, orig_XML_to_doc_obj
from typing import Dict, Tuple

def kansuji_to_num(x: str) -> int:
    """Convert a sequence of *kansuji* to the corresponding number.

    *Kansuji* is a representation of a number, which is used in Chinese and Japanese. This function converts a sequence of *kansuji* (a *kanji* string) to the corresponding number.

    Parameters
    ----------
    x : str
      A sequence of *kansuji*.

    Returns
    -------
    int
      The corresponding number for a given *kansuji* string.

    Examples
    --------
    >>> kawasemi.util.kansuji_to_num('三十五')
    35

    >>> kawasemi.util.kansuji_to_num('百六')
    106

"""
    
    result = 0
    
    if x == '' or x is None:
        return result
    
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
    
def lawNum_to_lawID(x: str) -> str:
    """Map a law number in Japan to the corresponding law ID.

    Each law in Japan has its unique law number. While a law number is an identifier, the *number* is difficult for a computer to deal with because the string consists of numbers and Chinese (*kanji*) characters. On the other hand, each law has its unique filename in the Japanese e-Gov database. We call such filenames law IDs for convenience.
    This function maps a law number to the corresponding law ID.

    Parameters
    ----------
    x : str
      A law number in Japan.

    Returns
    -------
    str
      The corresponding law ID.

    Examples
    --------
    >>> kawasemi.util.lawNum_to_lawID('明治二十九年法律第八十九号')
    129AC0000000089

    >>> kawasemi.util.kansuji_to_num('昭和四十五年法律第四十八号')
    345AC0000000048    

"""
    
    era2id = {'明治': 1, '大正': 2, '昭和': 3, '平成': 4, '令和': 5}
    lawtype2id = {'法律': 'AC'}
    
    m = re.match(r'(.{2})(.+)年(.+)第(.+)号', x)
    era = era2id[m.group(1)]
    year = kansuji_to_num(m.group(2).replace('元', '一'))
    lawtype = lawtype2id[m.group(3)]
    num = kansuji_to_num(m.group(4))

    return '{:3d}{:s}{:010d}'.format(era * 100 + year, lawtype, num)    

def make_law2lawNum_and_law2lawID(filename: str =None) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Create two dictionaries whose keys are law names.

    This function creates the following two dictionaries: 
    1. a dictionary of law numbers for law names, and
    2. a dictionary of law IDs for law names, 
    where law names as keys include abbreviated forms of official law names.

    Parameters
    ----------
    filename : str, optional
      A tsv file of (law name, law number) pairs. If it is None, the function uses the tsv file "abbr.tsv" in the data/utils directory.

    Returns
    -------
    law2lawNum : Dict[str, str]
      A dictionary of law numbers for law names.      
    law2lawID : Dict[str, str]
      A dictionary of law IDs for law names.

    Examples
    --------
    >>> law2lawNum, law2lawID = kawasemi.util.make_law2lawNum_and_law2lawID()
    >>> law2lawNum['民法']
    明治二十九年法律第八十九号
    >>> law2lawID['民法']
    129AC0000000089
    >>> law2lawNum['労働基準法']
    昭和二十二年法律第四十九号
    >>> law2lawNum['労基法']
    昭和二十二年法律第四十九号

"""
    
    if filename == None:
        filename = os.path.join(os.path.dirname(__file__),
                                '../../data/utils/abbr.tsv')     
    law2lawNum = {}
    law2lawID = {}
    
    with open(filename, 'r') as f:
        for line in csv.reader(f, delimiter='\t'):
            law2lawNum[line[0]] = line[1]
            law2lawID[line[0]] = lawNum_to_lawID(line[1])
    return law2lawNum, law2lawID
    
def load_model(lawname):
    """load model.

    under construction


    """
    
    law2lawNum, law2lawID = make_law2lawNum_and_law2lawID()
    
    try:
        lawID = law2lawID[lawname]
    except KeyError:
        print('You should input a valid law name in Japan.')
        exit()    
    tree = read_xml(lawID)


    
    return models.Statute(lawname)

