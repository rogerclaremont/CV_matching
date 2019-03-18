import os
import preprocessing as pp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import numpy as np
import collections


def plot_most_common_words(cv_path, stopwords):
	# Läser in word filer
	cv_list = []
	for subdir, dirs, files in os.walk(cv_path):
		for file in files:
			cv_filepath = subdir + os.sep + file
			cleaned_cv = pp.clean_text(pp.read_word_file(cv_filepath), stopwords)
			#lemmalized = pp.lemmatization_sv(cleaned_cv)
			#cv_list.append(lemmalized)
			cv_list.append(cleaned_cv)
	
	wordcount = {}
	for cv in cv_list:
		for word in cv.split():
			if word not in wordcount:
				wordcount[word] = 1
			else:
				wordcount[word] += 1
	
	word_counter = collections.Counter(wordcount)
	for word, count in word_counter.most_common(100):
		print(word, ": ", count)

def plot_cvs(cv_path, stopwords):
	"""
	Läser in alla word-filer som finns i mappen "cv_path" och visualiserar datan
	genom att göra en dimensionell reduktion till 2D och plotta både k-means kluster
	och alla bolag för sig. Argumentet "stopwords" ska vara en lista med sökvägar till
	text dokument innehållande de stoppord som önskas användas.
	"""
	
	# Läser in word filer och städar upp med angivna stoppord.
	cv_list = []
	lbl_indx = []
	lbl_cntr = -1
	dir_path = ''
	for subdir, dirs, files in os.walk(cv_path):
		for file in files:
			cv_filepath = subdir + os.sep + file
			if dir_path != subdir:
				lbl_cntr += 1
			cleaned_cv = pp.clean_text(pp.read_word_file(cv_filepath), stopwords)
			#lemmalized = pp.lemmatization_sv(cleaned_cv)
			#cv_list.append(lemmalized)
			cv_list.append(cleaned_cv)
			lbl_indx.append(lbl_cntr)
			dir_path = subdir

	# Skapar en TF-IDF vektor
	tfidf = TfidfVectorizer()
	tfidf_vector = tfidf.fit_transform(cv_list)

	# Hitta kluster med k-means
	km = KMeans(n_clusters=17, init='k-means++', max_iter=100, n_init=5, verbose=1)
	km.fit(tfidf_vector)

	# Dimensionell reduktion till 2D
	tfs_reduced = TruncatedSVD(n_components=17, random_state=0).fit_transform(tfidf_vector)
	tfs_embedded = TSNE(n_components=2, perplexity=40, verbose=2).fit_transform(tfs_reduced)

	# Plotta kluster
	fig = plt.figure(figsize = (10, 10))
	ax1 = plt.axes()
	plt.scatter(tfs_embedded[:, 0], tfs_embedded[:, 1], marker = "x", c = km.labels_)
	plt.show()
	plt.close()

	# Plotta olika bolag
	labels = ['CA', 'CAB', 'CAD', 'CBD', 'CBS', 'CBT', 'CDB', 'CDS', 'CEC', 'CED', 'CIM', 'CLD', 'CNP', 'CNS', 'CQM', 'CQS', 'CXD']
	markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', '+', 'x', 'X', 'D', '1', '2', '3', '4', '_']
	colors = cm.rainbow(np.linspace(0, 1, 18))
	fig = plt.figure(figsize = (10, 10))
	ax1 = plt.axes()
	lbl = labels[0]
	ax1.scatter(tfs_embedded[0, 0], tfs_embedded[0, 1], marker = markers[0], color = colors[lbl_indx[0]], label = lbl)
	for indx in range(1,len(tfs_embedded[:, 0])):
		if lbl == labels[lbl_indx[indx]]:
			ax1.scatter(tfs_embedded[indx, 0], tfs_embedded[indx, 1], marker = markers[lbl_indx[indx]], color = colors[lbl_indx[indx]])

		else:
			lbl = labels[lbl_indx[indx]]
			ax1.scatter(tfs_embedded[indx, 0], tfs_embedded[indx, 1], marker = markers[lbl_indx[indx]], color = colors[lbl_indx[indx]], label = lbl)
	ax1.legend()
	plt.show()




if __name__ == "__main__":
	plot_cvs('./data/CVs/Svenska', ['./data/stopwords_sv.txt', './data/remove_words.txt'])
	#plot_most_common_words('./data/CVs/Svenska', ['./data/stopwords_sv.txt', './data/remove_words.txt'])
	#print(pp.lemmatization_sv('test tests testas testades testade testet'))


#print(pp.read_word_file('./data/CVs/CIM/Svenska/CV_Claremont_Roger_Kalliomäki.docx'))








