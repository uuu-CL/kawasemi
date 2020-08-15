"""This module deals with UML diagrams, especially PlantUML formats, for a legal paragraph.
"""

import os

def make_uml(res):
    uml = ['@startuml', '', '!include conf.txt', '']
    N3s = []

    for tag in reversed(result.tag_list()):
        N3 = {'subject': 'A', 'object': 'B', 'predicate': 'None'}
        if tag.pas != None:
            N3['predicate'] = ''.join([mrph.midasi for mrph in tag.mrph_list()])
                       
            if 'ヲ' in tag.pas.arguments:
                arg = tag.pas.arguments['ヲ'][0]
                N3['object'] = arg.midasi
                
            if 'ガ' in tag.pas.arguments:
                arg = tag.pas.arguments['ガ'][0]
                N3['subject'] = arg.midasi
            
            N3s.append(' '.join([N3['subject'], '->', N3['object'], ':',
                                 N3['predicate']]))
                       
        
        else:
            for mrph in tag.mrph_list():
                if mrph.hinsi == '動詞':
                    N3['predicate'] = mrph.midasi
                    N3s.append(' '.join([N3['subject'], '->', N3['object'], ':',
                                         N3['predicate']]))
                    break

    
    # participants
    uml.append('actor Aさん as A <<当事者>>')
    uml.append('actor Bさん as B <<相手方>>')

    # actions
    for N3 in reversed(N3s):
        uml.append(N3)
       
    uml.extend(['', '@enduml'])
    return uml

def write_uml(uml, filename):
    with open(filename, 'w') as f:
        for line in uml:
            f.write(line)
            f.write('\n')

def show_uml(filename, plantuml='/usr/local/bin/plantuml'):
    import subprocess
    umldir = os.path.dirname(filename)    
    proc = subprocess.run([plantuml, filename], cwd=umldir,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE)
    print('done!')
    imgfile = filename.replace('.uml', '.png')

    from PIL import Image
    from matplotlib import pyplot as plt
    img = Image.open(imgfile)
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    ax.imshow(img)
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close('all')
               
if __name__ == '__main__':
    from tokens import JNLP
    nlp = JNLP()
    text = '詐欺又は強迫による意思表示は、取り消すことができる。'
    result = nlp.parse(text)
    uml = make_uml(result)
    indir = os.path.join(os.path.dirname(__file__), 
                         '../../data/UML')
    filename = os.path.join(indir, 'a.uml')
    write_uml(uml, filename)
    show_uml(filename)
            
    # print(tag.tag_id, tag.dpndtype, tag.parent_id, tag.fstring)
    # 
