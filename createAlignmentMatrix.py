import timeit
import string
import numpy
import sys
from phraseExtraction import extractPhrases

try:
	outputFileName = sys.argv[1] #output file where the english and german phrase pairs will be stored
	inputFileName1 = sys.argv[2] #alignment file from Giza++ for english to german translation
	inputFileName2 = sys.argv[3] #alignment file from Giza++ for german to english translation
except:
	print "Expected Parameters: outputFileName gizaInput1 gizaInput2"
	

outputFile = open(outputFileName,'w')
inputFile1 = open(inputFileName1,'r')
inputFile2 = open(inputFileName2,'r')

count = 0
def createMatrix(inputFile):

	#Extract foreign sentence and words
	foreignSentence = inputFile.readline().strip().lower()
	#foreignSentence = foreignSentence.translate(string.maketrans('',''), string.punctuation)
	foreignWords = foreignSentence.strip().split(' ')
	#print foreignSentence
	foreignSentenceLength = len(foreignWords)
	
	#Extract english sentence and words
	englishSentence = inputFile.readline().strip().lower()
	englishPairs1 = englishSentence.split('})')
	englishPairs = []
	englishWords = []
	#Split english pair of form: word ({ 1 2 }), into englishWord,alignment pair
	for englishPair in englishPairs1:
		englishPair = englishPair.split('({')
		if len(englishPair)>1:
			englishWord = englishPair[0].strip()
			
			alignment = englishPair[1]
			#skip if englishWord extract is null
			if englishWord!='null':
				englishPairs.append([englishWord, alignment])
				englishWords.append(englishWord)
	
	englishSentenceLength = len(englishPairs)

	#Initialise alignment matrix
	alignmentMatrix = numpy.zeros([englishSentenceLength,foreignSentenceLength]).astype(int)
	#populate the alignment matrix
	for i in range(0, len(englishPairs)):
		listing = englishPairs[i][1]
		listing = listing.strip().split(' ')
		for j in listing:
			if j!='':
				j = int(j)
				alignmentMatrix[i,j-1] = 1

	return alignmentMatrix,englishSentenceLength,foreignSentenceLength, foreignWords, englishWords
		

def multidim_or(arr1, arr2, size1, size2): #This function returns the union of two matrices
    arr1 = arr1.flatten()
    arr2 = arr2.flatten()
    or_arr = numpy.logical_or(arr1, arr2)
    or_arr = or_arr.reshape((size1, size2))
    return or_arr.astype(int)


start = timeit.default_timer()

while inputFile1.readline() and inputFile2.readline(): #Reading both the files together
	count += 1
	print count
	alignmentMatrix1,englishSentenceLength1,foreignSentenceLength1, foreignWords1, englishWords1 = createMatrix(inputFile1)
	alignmentMatrix2,englishSentenceLength2,foreignSentenceLength2, foreignWords2, englishWords2 = createMatrix(inputFile2)
	try:
		alignmentMatrix = multidim_or(alignmentMatrix1,numpy.transpose(alignmentMatrix2), englishSentenceLength1, foreignSentenceLength1)
	except:		
		continue

	extractPhrases(alignmentMatrix, englishSentenceLength1, foreignSentenceLength1, foreignWords1, englishWords1, outputFile)
end = timeit.default_timer()
print end - start
outputFile.close()
