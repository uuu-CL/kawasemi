"""This module provides functions for downloading files from web sites.
"""

import os
import requests
import zipfile
import time

def download_file(url: str, indir: str) -> str:
    """Download a file at a given URL and save it in a given directory.

    This function downloads a file from a web site and saves it in a directory. Then it returns the file path.

    Parameters
    ----------
    url : str
      A string of a URL.
    indir : str
      A directory name which will contain the downloaded file.

    Returns
    -------
    str
      The file path of the downloaded file.
      
    Examples
    --------
    >>> url = 'http://example/aaaa.zip'
    >>> indir = '/home/x/y/'
    >>> kawasemi.download.download_file(url, indir)
    /home/x/y/aaaa.zip

"""
    
    try:
        r = requests.get(url, stream=True)
        time.sleep(3)
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

def extract_zip(zipname: str) -> None:
    """Unzip a file.

    This function unzips a given zip file.

    Parameters
    ----------
    zipname : str
      A zip file from which you want to extract files.

    Returns
    -------
    None
      None.
      
    Examples
    --------
    >>> kawasemi.download.extract_zip('./aaaa.zip')

"""
    
    dirname = os.path.dirname(zipname)
    z = zipfile.ZipFile(zipname)
    z.extractall(dirname)
