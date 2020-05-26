import fasttext
from trumpDataset.basisFuncs import *

def writeCleanedTotxtFile(fileName = "trumpDataset/clean.txt"):
	f = open(fileName,"w")
	mycursor.execute("select id, cleanedText from " + mainTable + " " + relevancyDateThreshhold + " and isRt = 0")
	tweets = mycursor.fetchall()
	for tweet in tweets:
		cleanText = tweet[1]
		f.write(cleanText+"\n")


def computeWordEmbeddings(cleanFile = "trumpDataset/clean.txt", embeddingsFile = "trumpDataset/cleanModel.bin"):
	writeCleanedTotxtFile()
	try:
		model = fasttext.load_model(embeddingsFile)
	except:
		model = fasttext.train_unsupervised(cleanFile, model='cbow', minCount = 1)
		for word in model.words[:20]:
			print(model[word])

		model.save_model(embeddingsFile)
	return model



def getTopNVectorsForTweet(model, tweetText, n, vectorLen):
	vecs = []

	nlpTweetText = nlp(tweetText)

	words = [str(token) for token in nlpTweetText if not unworthynessOfToken(token)]

	wordsInDescendingFrequencyFile =open("trumpDataset/npStores/wordsInDescendingFrequency.p","rb")
	wordsInDescendingFrequency = pickle.load(wordsInDescendingFrequencyFile);
	wordsInDescendingFrequency = [word[0] for word in wordsInDescendingFrequency]
	topNIndices = []
	for word in words:
		if word in wordsInDescendingFrequency:
			topNIndices.append(wordsInDescendingFrequency.index(word))
		else:
			print("bust |"+word+"|")
	topNIndices.sort()
	topNIndices = topNIndices[:n]



	topNWords = [wordsInDescendingFrequency[index] for index in topNIndices]#TODO top n words for tweetText

	for word in topNWords:
		vec = model[word]
		vecs.append(vec)
	if len(vecs)<5:
		print("proppin that up what " ,len(vecs),topNWords)
	while len(vecs) < 5:
		vecs.append(np.zeros((vectorLen)))

	return vecs;





