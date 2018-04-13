import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score
from sklearn import svm
from sklearn import metrics
text_data = []
event_data = []

#----------------------------------------------------------------------
def csv_dict_reader(file_obj):
	"""
	Read a CSV file using csv.DictReader
	"""
	reader = csv.DictReader(file_obj, delimiter=',')
	for line in reader:
		text_data.append(line['text'])
		event_data.append(int(line['event_type']))
#----------------------------------------------------------------------

with open("./football-events/events.csv") as f_obj:
	csv_dict_reader(f_obj)

total =  len(text_data)
train_size = int(0.75*total)
print train_size
train_data = text_data[ : train_size]
train_events = event_data[ : train_size]

test_data = text_data[train_size : ]  
test_events = event_data[train_size : ]

clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2), max_features=6000000)), ('tfidf', TfidfTransformer(sublinear_tf=True)), ('clf', svm.LinearSVC(max_iter=50, class_weight='balanced'))])
# clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer(sublinear_tf=True)), ('clf', svm.LinearSVC(max_iter=50, class_weight='balanced'))])
clf.fit(train_data, train_events)

print "Model Trained"
predicted = clf.predict(test_data)
print "Predictions"

# print f1_score(test_events, predicted, average='macro')
print metrics.confusion_matrix(test_events, predicted)
print metrics.classification_report(test_events, predicted, target_names=["Announcement", "Attempt", "Corner", "Foul", "Yellow card", "Second yellow card", "Red card", "Substitution", "Free kick won", "Offside", "Hand ball", "Penalty conceded"])


