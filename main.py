import os
import re
import datetime
# import shutil
import urllib.request as urllib
import subprocess




def processTY(f,lines):
    for line in f:
        if line[:1] == "#":
            break 
    return False 
    
def processKA(f,lines): 
    for line in f:
        if line[:1] == "#":
            break 
    return False 

def processKD(f,lines):
    for line in f:
        if line[:1] == "#":
            break 
    return False 

def processZA(f,lines):   
    for line in f:
        if line[:1] == "#":
            break 
    return False 
    
def processZP(f,lines): 
    for line in f:
        if line[:1] == "#":
            break 
    return False 

def processSM(f,lines):   
    for line in f:
        if line[:1] == "#":
            break 
    return False 
  
def processLL(f,lines):
    for line in f:
        if line[:1] == "#":
            break 
    return False 
def processWK(f,numer_lini):
    for line in f:
        if line[:1] == "#":
            break 
    return False 
           
    
def readlines(f,name):
    """ Iterate lines from an archive member. """
    linesep = os.linesep[-1]
    line = ''
    for ch in f.bytestream(name):
        line += ch
        if ch == linesep:
            yield line.decode("cp1250").encode('utf-8')
            line = ''
    if line: yield line.decode("cp1250").encode('utf-8')


def parse_file(directory,filename):
    with open(filename,"r") as f:
        fo = f.readlines()
    
    retcode = False
    for line in fo:
        print(line[1:3])
        if line[1:3] == "##":
            break
        
        print('process' + line[1:3] +'(fo,' + line[4:]+')')
        retcode = eval('process' + line[1:3] +'(fo,' + line[4:]+')')
        if retcode:
            break

def download_now():
    import datetime
    import urllib.request as urllib

    now = datetime.datetime.now()
    now_str = now.strftime("%y%m%d")

    url = "ftp://rozklady.ztm.waw.pl/RA" + now_str + ".7z"

    try:
        urllib.urlretrieve(url, "archive.7z")
    except Exception as e:
        print(str(e))
        
def unzip_download(file_name = "archive.7z"):
    import os, subprocess

    cwd = os.getcwd()
    file_path = os.path.join(cwd,file_name)
    
    print(file_path)

    subprocess.call(["C:/Program Files/7-Zip/7z.exe", 'e', "-o" + cwd, file_path])
    
    os.remove(file_path)
    print("File Removed!")



class SevenZFile(object):



    @classmethod
    def is_7zfile(cls, filepath):
        """ Determine if filepath points to a valid 7z archive. """
        is7z = False
        fp = None
        try:
            fp = open(filepath, 'rb')
            #archive = py7zlib.Archive7z(fp)
            is7z = True
        finally:
            if fp: fp.close()
        return is7z

    def __init__(self, filepath):
        fp = open(filepath, 'rb')
        self.filepath = filepath
        self.archive = py7zlib.Archive7z(fp)

    def __contains__(self, name):
        return name in self.archive.getnames()

    def bytestream(self, name):
        """ Iterate stream of bytes from an archive member. """
        if name not in self:
            raise SevenZFileError('member %s not found in %s' %
                                  (name, self.filepath))
        else:
            member = self.archive.getmember(name)
            for byte in member.read():
                if not byte: break
                yield byte

    def readlines(self, name):
        """ Iterate lines from an archive member. """
        linesep = os.linesep[-1]
        line = ''
        for ch in self.bytestream(name):
            line += ch
            if ch == linesep:
                yield line.decode("cp1250").encode('utf-8')
                line = ''
        if line: yield line.decode("cp1250").encode('utf-8')


def download_7zfile(new = False):
	now = datetime.datetime.now()
	now_int = now.strftime("%y%m%d")

	h_local = os.getcwd() + '/files'
	h_local_files = []

	if os.listdir(h_local) == [] or new:
		latest_file = f"RA{now_int}.7z"
	else:
	    for file_name in os.listdir(h_local):
	    	h_local_files.append(file_name)
	    latest_file = sorted(h_local_files)[0]
	
	print(latest_file)

	if latest_file in h_local_files:
	    print("Local directory already contains latest file: " + latest_file)
	else:
	    print("Downloading latest 7z file...")

	    url = "ftp://rozklady.ztm.waw.pl/" + latest_file
	    try:
	        urllib.urlretrieve(url, os.path.join(h_local,latest_file))
	        print("File successfully downloaded.")
	    except Exception as e:
	        print(str(e))

	return(latest_file)

if __name__ == "__main__": 
    latest_file = download_7zfile()
    print(latest_file)
    file_path = os.path.join(os.getcwd(),'files',latest_file)
    subprocess.call(["C:/Program Files/7-Zip/7z.exe", 'e', "-o" + os.path.join(os.getcwd(),'files'), file_path])
	       

