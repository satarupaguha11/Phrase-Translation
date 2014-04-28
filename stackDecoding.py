import string
import sys
from collections import defaultdict
def extractProbabilityIntoDictionary(inputFile): #loading the phrase translation probabilities from file to a dictionary
	dictionary = defaultdict(lambda: defaultdict(float))
	for line in inputFile:
		line = line.split('\t')
		englishPhrase = line[0]
		foreignPhrase = line[1]
		probability = float(line[2].strip())
		dictionary[englishPhrase][foreignPhrase] = probability
	return dictionary

def findCombinations(index,inputWords): #find phrases of size 1,2, 3 and so on from a given sentence
	sentenceLength = len(inputWords)
	setOfWords = []
	for wordIndex in range(len(inputWords)):
		if wordIndex == sentenceLength - 1 - index:
			break
		phrase = ''
		#setOfWords.append(inputWords[wordIndex])
		for adjWordIndex in range(index+1):
			phrase = phrase+' '+inputWords[wordIndex+adjWordIndex]

		setOfWords.append(phrase.strip(' '))
	return setOfWords
			
def findHighestProbability(englishPhrase, dictionary): #find the foreign phrase which occurs with the highest probability for a given english phrase
	highestProbability = 0
	if not dictionary.has_key(englishPhrase):
		return ''
	#print "hello"
	for foreignPhrase in dictionary[englishPhrase]:
		if dictionary[englishPhrase][foreignPhrase]>highestProbability:
			highestProbability = dictionary[englishPhrase][foreignPhrase]
			bestForeignPhrase = foreignPhrase
			#print foreignPhrase
	return (bestForeignPhrase,highestProbability)

	

def formSentence(words,translation): #stick together words to form sentence
	sentence = ''
	sentenceLength = len(words)
	for wordIndex in range(len(words)):
		if translation[words[wordIndex]] != '':
			if wordIndex == (sentenceLength - 1):

				sentence = sentence+translation[words[wordIndex]]+'.'
			else:
				sentence = sentence+translation[words[wordIndex]]+' '
	return sentence

def stackDecoding(inputSentence, dictionary):
	inputSentence = inputSentence.lower().strip().translate(string.maketrans('',''), string.punctuation)
	inputWords = inputSentence.split(' ')

	numberOfStacks = len(inputWords)
	if numberOfStacks > 20:
		numberOfStacks = 20
	stack = {}
	score = {}
	for index in range(numberOfStacks):
		#print index
		stack[index] = []
		combinations = findCombinations(index,inputWords)
		#print combinations
		for item in combinations:
			stack[index].append(item)

	translation = defaultdict(lambda: defaultdict(str))
	for index in range(numberOfStacks):
		score[index] = 0

		for item in stack[index]:
			result = findHighestProbability(item, dictionary)
			if result != '':
				bestForeignPhrase = result[0]
				translation[index][item] = bestForeignPhrase
				probability = result[1]
				score[index] += probability
			else:
				pass
	#higestScoreStack = score.index(max([score[index] for index in range(numberOfStacks)]))
	maxScore = 0
	flag = 0
	for index in score:
		if score[index]>maxScore:
			flag = 1
			maxScore = score[index]
			bestIndex = index
	if flag == 1:
		outputSentence = formSentence(stack[bestIndex], translation[bestIndex])
	else:
		outputSentence = formSentence(stack[0], translation[0])
	return outputSentence

if __name__ == '__main__':
	try:
		inputFileName = sys.argv[1]
		inputSentence = sys.argv[2]
	except:
		print "Expected parameters: translationProbabilitiesFile testSentence"
		
	
	inputFile = open(inputFileName,'r')
	dictionary = extractProbabilityIntoDictionary(inputFile)
	outputSentence = stackDecoding(inputSentence, dictionary)
	print outputSentence



