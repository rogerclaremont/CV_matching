import re

def clean_text(text, stopwords):
	"""
	Rensar textsträngen "text" på stop-ord (givna i listan "stopwords"), samt allt utom bokstäver,
	och gör om versaler till gemener.
	"""
	only_letters = re.sub('[^a-zA-ZåäöÅÄÖ]', ' ', text)
	words = only_letters.lower().split()
	useful_words = [x for x in words if not x in stopwords]
	useful_words_string = ' '.join(useful_words)
	return useful_words_string


def read_mail_data(raw_data):
	"""
	Läser in text filen "raw_data" innehållande flera mail-dokument vilka separeras och
	retuneras som en lista med python dicts med formatet:
	mail_dict =	{
		"sender": "avsändarens epost-adress",
		"time": "datum och tid",
		"reciever": "mottagarens epost-adress",
		"subject": "ämne",
		"message": "meddelandet i eposten"
		}
	"""
	
	# Läs in epost-dataset utan föregående och efterliggande "whitespaces"
	with open(raw_data) as f:
		content = f.readlines()
	content = [x.strip() for x in content]
	
	# Dela upp alla mail med hjälp av "Från:-taggen" (skippa första "Från:-taggen"), ta bort alla tomma rader
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
		
	# Skapa en dict för varje mail och spara i en lista med dicts
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
	text_file = open('./data/stopwords.txt', 'r')
	stopwords_en = text_file.read().splitlines()
	text_file.close()
	text_file = open('./data/stoppord.txt', 'r')
	stopwords_sv = text_file.read().splitlines()
	text_file.close()
	stopwords = stopwords_en + stopwords_sv
	mails = read_mail_data('./data/job_ad_mails.txt')
	print(mails[99]['message'])
	print()
	print(clean_text(mails[99]['message'], stopwords))
