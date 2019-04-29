import os
import re
import datetime
import hashlib
import urllib.request as urllib
import subprocess
from pdb import set_trace as bp




	 
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
	global wrong_stops,result_directory,debug_directory

	stops_file = open('results/stops.txt','w')
	stops_file.write("stop_id,stop_name,stop_lon,stop_lat\n")

	wrong_stops = dict()
	print("Parsing section ZA - stops"  )
	nazwa = ''
	p = re.compile(".*Y= (\S*)\s*X= (\S*)")
	for line in f:
		
		if line[:1] == "#":
			break
		#print line[3:4]
		if line[3:4].isdigit():
			n = line[10:].split(',')
			if len(n) < 2:
				n=line[10:].split("--")
			nazwa = n[0]
			wstop = dict()
			lat = 0.0
			lon = 0.0
			i = 0
			next(f)
			for line in f:
				if line[9:10].isdigit():
					
					
					m = p.match(line[16:])
					if m:
						lat = lat + float(m.group(1))
						lon = lon + float(m.group(2))
						i = i+1
						stops_file.write(line[9:15] + ',' + nazwa + " "+ line[13:15] + "," + m.group(1) + ',' + m.group(2) + "\n")
					else:
						wstop[line[9:15]] = line[9:]
  
				if line[6:7] == "#":
					if i==0:
						wrong_stops.update(wstop)
						for key in wstop.keys():
							print(key+ ',' + nazwa + " "+ key[4:6] + ","  + ',')
						
					else:
						for key in wstop.keys():
							stops_file.write(key+ ',' + nazwa + " "+ key[4:6] + ","  + str(lat/i) + ',' + str(lon/i) +"\n")
							
					break    
	print("wrong stops size " + str(len(wrong_stops))) 
	return False 

def processSM(f,lines):   
	for line in f:
		if line[:1] == "#":
			break 
	return False 
  

def write_stop_times(tsfile, times_list, trip_id):
    i=1
    for tl in times_list:
        time = str(tl[1]).replace(".",":")
        tsfile.write(str(trip_id)+","+time+":00," +time+":00,"+tl[0] +","+str(i) +"\n")
        i = i+1

def processLL(f,lines):
	global trips_file,stop_times_file

	print("Parsing section LL - routes and times ") 

	stop_times_file = open('results/stop_times.txt','w')
	trips_file = open('results/trips.txt','w')

	stop_times_file.write("trip_id,arrival_time,departure_time,stop_id,stop_sequence\n")
	trips_file.write("route_id,service_id,trip_id\n")

	counter = 0 
	infolinia = ""
	for line in f:
		if line[3:6] == "Lin":
			infolinia =  line.rstrip().split()
			print("Parsing line: " + line)
			next(f)
				   
			processWK(f,infolinia[1])
			
		if counter > 10000000:
			break
		counter = counter+1
		if line[:1] == "#":
			break
	return False 

def processWK(f,numer_lini):
	global kursy_counter, dane_counter, trips_sums, trips_file,stop_times_file
	# tsum_counter = len(trips_sums)
	for line in f:
		if line[6:9] == "*WK":
			#print line
			# bp()
			kursy = dict()
			przebieg_kursu = list()
			
			m = hashlib.md5()

			for line in f:
				if line[6:9] == "#WK":
						break
				
				pola = line.split()

				if(pola[0] in kursy):
					m.update(pola[1].encode('utf-8'))
					przebieg_kursu.append([pola[1],pola[3]])
				else:
					kursy_counter = kursy_counter+1
					przebieg_kursu = list()
					m = hashlib.md5()
					m.update(pola[1].encode('utf-8'))
					m.update(pola[2].encode('utf-8'))
					przebieg_kursu.append([pola[1],pola[3]])
					kursy[pola[0]] = kursy_counter
						
				if len(pola)==5:
					if (pola[4]=="P"):
						if (m.digest() in trips_sums):
							t = trips_sums[m.digest()] 
							write_stop_times(stop_times_file, przebieg_kursu, t)
		
						else:
							# nalezy dodac nowy wpis do trips
							tid =len(trips_sums)+1 
							trips_file.write(numer_lini +"," + pola[2] + "," + str(tid) + "\n")
							trips_sums[m.digest()] =  tid
							
							# zapisac rekordy w trip_tops
							write_stop_times(stop_times_file, przebieg_kursu, tid)
				
				dane_counter=dane_counter+1  
			  
			break    
	 
	 
def read_large_file(file_object):
	"""
	Uses a generator to read a large file lazily
	"""
		
	linesep = os.linesep[-1]
	
	while True:
		data = file_object.readline()
		if not data:
			break
		yield data.rstrip(linesep)

		
		
def parse_file(filename):
	with open(filename,"r",encoding = 'cp1250') as f:
		fo = read_large_file(f)
	
		retcode = False
		for line in fo:
			# print(line[1:3])
			if line[1:3] == "##":
				break
			
			# print('process' + line[1:3] +'(fo,' + line[4:]+')')
			retcode = eval('process' + line[1:3] +'(fo,' + line[4:]+')')
			if retcode:
				break


if __name__ == "__main__": 
	if not os.path.exists(os.getcwd() + "/files"):
		os.makedirs(os.getcwd() + "/files") 

	if not os.path.exists(os.getcwd() + "/results"):
		os.makedirs(os.getcwd() + "/results") 	

	# check for existing files or append a new one
	latest_file = download_7zfile(new = False)
	print(latest_file)

	# unzip the file using system cmd 7z
	file_path = os.path.join(os.getcwd(),'files',latest_file)
	subprocess.call(["C:/Program Files/7-Zip/7z.exe", 'e', "-o" + os.path.join(os.getcwd(),'files'), file_path, "-aos"])
	
	kursy_counter=1
	dane_counter=0
	trips_sums = dict()

	parse_file(file_path[:-2] + "txt")
	

