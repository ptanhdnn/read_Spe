import numpy as np
import pandas as pd
import glob
import os

def get_data(file): #get data
	data_ele = []
	infile = open(file,'r')
	with open(file, 'r') as f:
		data = [s.strip() for s in f.readlines()]

		for i in range(12,2060):
			data_ele.append(data[i])
		return data_ele

def data_2_df(file_path):
	'''
	transform data to df from each "*.spe" data file and merge together
	Note merge by index after transpose
	'''
	output = pd.DataFrame()
	dict_list = {file[:-4]:get_data(file) for file in file_path}	#dict
	dic = pd.DataFrame(dict_list)
	output = pd.concat([output, dic], axis = 0, ignore_index = True)
	output = output.reindex(sorted(output.columns, key = lambda s:int(s.replace('run', ''))), axis = 1)
	output = output.T
	return output, dict_list

def create_source(logf_path, df, list_name):
	'''
	cut source data from logfile
	'''
	source_logfile = pd.read_excel(logf_path, sheet_name = 1, skiprows = 1,
								).loc[:len(df)-1,['Tên file','Cs-137','Co-60','Am-241','RGU','RGTh','RGK']]
#	source_logfile = source_logfile.rename(columns = {'Tên file':'file name'})
	source_logfile = source_logfile.set_index('Tên file')
	return source_logfile


index = []
if __name__ == "__main__":
	old_path = os.getcwd()
	path = './file_spe'
	os.chdir(path)									#change to directory
	file_path = glob.glob('*.Spe')
	logf_path = './LogFileForGML(1).xlsx'
	df, name_file_list = data_2_df(file_path)
	source = create_source(logf_path, df, name_file_list)
	data = pd.concat([df,source], axis = 1)
	data.index = sorted(data.index.values, key = lambda s:int(s.replace('run', '')))
	os.chdir(old_path)								#get back directory
	data.to_csv("Data_final.csv", index = True)
	print("done!!!")