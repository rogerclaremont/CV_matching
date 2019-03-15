from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import preprocessing as pp

STOPWORD_PATHS = ['./data/stopwords_en.txt', './data/stopwords_sv.txt']
DATA_PATH = './data/job_ad_mails.txt'
TEST_CV_TEXT = 'Joakim är en verksamhetsorienterad konsult inom Microsoft Dynamics 365 med CRM som huvudområde. Han har lång erfarenhet av att implementera CRM inom flera sektorer som en Web/Mobil/Kontaktcenter-lösning och har bl.a. lett ett flertal globala utrullningsprojekt (det största för +1100 användare i över 25 länder).  	Microsoft Dynamics 365 Resco Mobile CRM Verksamhet & processmodellering Kravhantering Lösningsdesign projektledning Testledning	Rådgivning 	Utrullning KURSER/CERTIFIKAT 	Microsoft Dynamics CRM 2015 Applications 	Microsoft Dynamics CRM 2011 Applications 	Microsoft Dynamics CRM 2011 Customization & Configuration 	Siebel 8 Consultant Certified Expert ANSTÄLLNINGAR Claremont Dynamics AB – Projektledare/Business Analyst Microsoft Dynamics 365 Avanade Sweden AB – Projektledare/Business Analyst Microsoft Dynamics 365 Tieto Sweden AB –Business Analyst Microsoft Dynamics 365SPRÅK svenska - modersmål 	Engelska – flytande Joakim var ansvarig för att rulla ut ett nytt Säljstöd baserat på Dynamics 365 V9 och Dynamics egna mobilapplikation till 4 regioner i Europa och Nordamerika. Ansvarsområden inkluderade bl.a. teknisk och funktionell verifiering av systemet, slutanvändarutbildning samt användarstöd under och i anslutning till utrullning. Joakim hade huvudansvaret som Lead Business Analyst och Projektledare under ett implementationsprojekt av ett Sälj- och Kundtjänststöd för en global tillverkare av produkter inom byggnadsindustrin. Lösningen baserades på Dynamics CRM Online och Dynamics egna mobilapplikation och rullades ut i 15 länder spridda över Europa, Asien och Amerika. I samband med utrullningsprojektet tog man också beslut om att uppgradera lösningen från Dynamics CRM 2011 On-Premise till Dynamics CRM Online. Joakim hade huvudansvaret för den funktionella sidan av uppgraderingen vilket inkluderade exempelvis workshop-planering och utförande, kravinsamling och lösningsdesign. Han ledde även testerna samt höll i slutanvändarutbildningar i den uppgraderade lösningen. Joakim hade huvudansvaret som Lead Business Analyst under ett implementationsprojekt av ett Sälj- och Kundtjänststöd för en global tillverkare av utomhusprodukter. Lösningen baserades på Dynamics CRM 2011 On-Premise, Resco Mobile CRM och Microsofts Unified Service Desk och rullades ut till +1100 användare i över 25 länder världen över. Joakims uppgifter innefattade bl.a. att leda utrullningsteamet och vara på plats under alla utrullningar för att förbereda både system och användare (exempelvis med datavalidering, utbildning och användarstöd) och ansvar för överlämning till supportorganisation efter avslutad utrullning.'
TEST_CV = pp.clean_text(TEST_CV_TEXT, STOPWORD_PATHS)

all_mail_data = pp.read_mail_data(DATA_PATH)
cleaned_messages = [TEST_CV]
for mail in all_mail_data:
	cleaned_messages.append(pp.clean_text(mail['message'], STOPWORD_PATHS))

tfidf = TfidfVectorizer()
tfidf_vector = tfidf.fit_transform(cleaned_messages)

model_tf_idf = NearestNeighbors(metric='cosine', algorithm='brute')
model_tf_idf.fit(tfidf_vector)

query_tf_idf = tfidf_vector[0]
distances, indices = model_tf_idf.kneighbors(query_tf_idf, n_neighbors=4)

for indx in indices.flatten():
	print(all_mail_data[indx]['message'])
	print()