import os
import requests
import zipfile

def download_file(url, indir):
    try:
        r = requests.get(url, stream=True)
    except:
        print('Could not download the original XML file from the e-Gov site.')
        exit()
    
    filename = url.split('/')[-1]
    path = os.path.join(indir, filename)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        return path

def extract_zip(zipname):
    dirname = os.path.dirname(zipname)
    z = zipfile.ZipFile(zipname)
    z.extractall(dirname)


