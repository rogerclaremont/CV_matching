import re
import docx
import spacy
from spacy.lang.sv import Swedish

def lemmatization_sv(text):
	"""
	Returnerar en lista med orden i givna strängen i grundform.
	"""
	nlp = Swedish()
	tokenized = nlp(text)
	lemmalized = [token.lemma_ for token in tokenized]
	lemmalized_words_string = ' '.join(lemmalized)
	return lemmalized_words_string

def clean_text(text, stopword_paths):
	"""
	Rensar textsträngen "text" på allt utom bokstäver och alla stop-ord givna i textfilen/textfiler 
	givna i listan "stopword_paths", samt gör om versaler till gemener.
	TODO - separera engelska och svenska
	"""
	stopwords = []
	for stop_path in stopword_paths:
		text_file = open(stop_path, 'r')
		stpwrds = text_file.read().splitlines()
		stopwords += stpwrds
		text_file.close()
	only_letters = re.sub('[^a-zA-ZåäöÅÄÖ]', ' ', text)
	words = only_letters.lower().split()
	useful_words = [x for x in words if not x in stopwords]
	useful_words_string = ' '.join(useful_words)
	return useful_words_string

def read_word_file(word_file):
	"""
	Läser in en word filen "word_file" och retunerar innhehållet som en sträng.
	"""
	doc = docx.Document(word_file)
	fullText = []
	for para in doc.paragraphs:
		fullText.append(para.text)
	return '\n'.join(fullText)

def read_mail_data(raw_data):
	"""
	Läser in text filen "raw_data" innehållande flera mail-dokument vilka separeras och
	returneras som en lista med Python-dicts med formatet:
	mail_dict =	{
		"sender": "avsändarens epost-adress",
		"time": "datum och tid",
		"reciever": "mottagarens epost-adress",
		"subject": "ämne",
		"message": "meddelandet i eposten"
		}
	"""
	
	# Läs in e-post-dataset utan föregående och efterliggande "whitespaces"
	with open(raw_data) as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	
	# Dela upp all e-post med hjälp av "Från:-taggen" (skippa första "Från:-taggen"), ta bort alla tomma rader
	mail_lists = []
	mail = []
	words = content[0].split()
	mail.append(' '.join(words))
	for line in content[1:]:
		if not line:
			continue
		words = line.split()
		if words[0]=='Från:':
			mail_lists.append(mail)
			mail = []
		mail.append(' '.join(words))
		
	# Skapa en dict för varje e-post och spara i en lista med dicts
	mail_dicts = []
	mail_dict =	{}
	for mail_list in mail_lists:
		mail_dict['sender'] = mail_list[0]
		mail_dict['time'] = mail_list[1]
		mail_dict['reciever'] = mail_list[2]
		mail_dict['subject'] = mail_list[3]
		mail_dict['message'] = mail_list[4]
		for message_line in mail_list[5:]:
			mail_dict['message'] = mail_dict['message'] + ' ' + message_line
		mail_dicts.append(mail_dict)
		mail_dict =	{}

	return mail_dicts


if __name__ == "__main__":
	mails = read_mail_data('./data/job_ad_mails.txt')
	print(mails[99]['message'])
	print()
	stopword_paths = ['./data/stopwords_en.txt', './data/stopwords_sv.txt']
	print(clean_text(mails[99]['message'], stopword_paths))
