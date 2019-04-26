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
     

	 
def read_large_file(file_object):
    """
    Uses a generator to read a large file lazily
    """
    while True:
        data = file_object.readline()
        if not data:
            break
        yield data

def parse_file(filename):
    with open(filename,"r") as f:
        fo = read_large_file()
    
    retcode = False
    for line in fo:
        print(line[1:3])
        if line[1:3] == "##":
            break
        
        print('process' + line[1:3] +'(fo,' + line[4:]+')')
        retcode = eval('process' + line[1:3] +'(fo,' + line[4:]+')')
        if retcode:
            break






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
    # check for existing files or append a new one
    latest_file = download_7zfile(new = False)
    print(latest_file)

    # unzip the file using system cmd 7z
    file_path = os.path.join(os.getcwd(),'files',latest_file)
    subprocess.call(["C:/Program Files/7-Zip/7z.exe", 'e', "-o" + os.path.join(os.getcwd(),'files'), file_path, "-aos"])

    with open(file_path[:-2] + "txt","r") as f:
        fo = f.readlines()
        
        retcode = False
        for line in fo:
            print(line[1:3])
            if line[1:3] == "##":
                break
            retcode = eval('process' + line[1:3] +'(fo,' + line[4:]+')')
            if retcode:
                break
			


	       

