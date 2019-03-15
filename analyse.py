import os
import preprocessing as pp

STOPWORD_PATHS = ['./data/stopwords_sv.txt']


for subdir, dirs, files in os.walk('./data/CVs'):
	for file in files:
		filepath = subdir + os.sep + file
		print(subdir[11:14])
		
print(pp.read_word_file('./data/CVs/CIM/Svenska/CV_Claremont_Roger_Kalliomäki.docx'))