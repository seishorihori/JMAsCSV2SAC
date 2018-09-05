"""
> convert JMA CSV file(s) to SAC files 

> for strong motion records obtained with seismic intensity meters 
installed by local goverments

> coded by Haruo Horikawa

"""

import sys
import glob
import time
import datetime
import numpy as np
import obspy
#from obspy.signal.trigger import pk_baer

###
def GetCSVFileList(Dir):
	CSVFiles = glob.glob(Dir+'/acc*.csv')

	return CSVFiles

###
def ReadCSVFiles(Dir):
	iunit = open(CSVFile, 'r', encoding='shift_jis')

# get header values
	NSsampling, EWsampling, UDsampling, TriggerTime, StnCode, StnLon, StnLat = GetHeaderValues(iunit)
	print(TriggerTime)

# get body or raw data
	NSdigit, EWdigit, UDdigit = GetRawData(iunit)

#	sys.exit()

	return NSdigit, EWdigit, UDdigit, NSsampling, EWsampling, UDsampling, TriggerTime, StnCode, StnLon, StnLat

##
def GetHeaderValues(iunit):

# get Station Code
	line = iunit.readline()
	StnCode = line[11:16]
	print(StnCode)

# get staion location (longitude, latitude)
	line = iunit.readline()
	tmp = line.split()
	StnLat = float(tmp[1])

	line = iunit.readline()
	tmp = line.split()
	StnLon = float(tmp[1])

# get sampling rate
	line = iunit.readline()
	tmp = line.split("=")
	HzIndex = tmp[1].index("Hz")
#	print(HzIndex)
	SamplingRate = tmp[1][0:HzIndex]
	print(SamplingRate)
	NSsampling = int(SamplingRate)
	EWsampling = int(SamplingRate)
	UDsampling = int(SamplingRate)

# read one line that show physical unit, but not do anything
	line = iunit.readline()

# get trigger time
	line = iunit.readline()
	tmp = line.split()
	TriggerTime = []
	for tmp_index in range(6):
#		print(tmp_index, tmp[tmp_index+3])
		TriggerTime.append(int(tmp[tmp_index+3]))

#	sys.exit()
	return NSsampling, EWsampling, UDsampling, TriggerTime, StnCode, StnLon, StnLat

##
def GetRawData(iunit):
	line = iunit.readline()
	NSdigit = []
	EWdigit = []
	UDdigit = []
	for line in iunit.readlines():
#		print(line)
		tmp = line.strip().split(",")
#		print(tmp)
		NSdigit.append(tmp[0])
		EWdigit.append(tmp[1])
		UDdigit.append(tmp[2])

	return 	NSdigit, EWdigit, UDdigit
#
###
#
if __name__ == '__main__':
#
	comp = ['.n', '.e', '.z']
	cmpaz = [0., 90., 0.]
	cmpinc = [90., 90., 0.]

#
	DIR00 = '/Volumes/DATA01/JMA/strong_motion/2018/20180618_0758/jichitai/'

	CSVFiles = GetCSVFileList(DIR00)
	print(CSVFiles)

### make SACfiles CSV file by CSV file
	for CSVFile in CSVFiles:

# read CSV file(s)
#		NSdigit, EWdigit, UDdigit, NSsampling, EWsampling, UDsampling, TriggerTime = ReadCSVFiles(DIR00, StnCode, hhmm)
		NSdigit, EWdigit, UDdigit, NSsampling, EWsampling, UDsampling, TriggerTime, StnCode, StnLon, StnLat = ReadCSVFiles(CSVFile)
		print(type(NSdigit))
		sampling = np.array([NSsampling, EWsampling, UDsampling])
		digit = np.array([NSdigit, EWdigit, UDdigit])

# pick P-wave arrival
#		p_baer, phase_info_baer = pk_baer(UDdigit, UDsampling, 20, 60, 7.0, 12.0, 100, 100)
#		print('Acc:', p_baer/UDsampling, phase_info_baer)

#		P_ArrivalTime = list(TriggerTime)

# calculate date and time of P-arrival
		nsec = TriggerTime[5]
		nmsec = 0

		Trigger_Date = datetime.datetime(TriggerTime[0], TriggerTime[1], TriggerTime[2], TriggerTime[3], TriggerTime[4], nsec, 1000*nmsec)
		print("Trigger Date:", Trigger_Date)
		p_baer_Date = datetime.timedelta(milliseconds=int(10*p_baer))
		P_ArrivalTime_Date = Trigger_Date + p_baer_Date
		print("P-arrival Date and Time:", P_ArrivalTime_Date)

# create the base part of header
#		print(TriggerTime)
		yyyymmdd = str(TriggerTime[0]) + '.' + str(TriggerTime[1]) + '.' + str(TriggerTime[2])
		day_of_year = time.strptime(yyyymmdd, "%Y.%m.%d").tm_yday
#print(day_of_year)

		cyyyymmdd = Trigger_Date.strftime('%Y%m%d')
		chhmm = Trigger_Date.strftime('%H%M')
		print(cyyyymmdd)
		print(chhmm)

		header_base = { 'kstnm': StnCode, 'stla': StnLat, 'stlo': StnLon, \
		'nzyear': TriggerTime[0], 'nzjday': day_of_year, \
		'nzhour': TriggerTime[3], 'nzmin': TriggerTime[4], \
		'nzsec': nsec, 'nzmsec': nmsec}

# create SAC files, adding appropriate header values

		for icomp in range(3):
			header = header_base
	
			header['delta'] = 1.0/sampling[icomp]
			header['cmpaz'] = cmpaz[icomp]
			header['cmpinc'] = cmpinc[icomp]

			print(header)

			aho = obspy.io.sac.SACTrace(data=digit[icomp,:], **header)

#	SACFileName = 'ahoaho' + comp[icomp]
			SACFileName = 'LG' + StnCode + '.' + cyyyymmdd + '.' + chhmm + comp[icomp]
			aho.write(SACFileName, byteorder='big')


