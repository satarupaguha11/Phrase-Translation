from collections import defaultdict
import sys
#initialize dictionary
countDictionary = defaultdict(lambda: defaultdict(int))

#output file where the probabilities will be written
#outputFile = open('phraseTranslationProbabilityTable_20000.txt','w')

try:
	outputFileName = sys.argv[1]
	filename = sys.argv[2]
except:
	print "Expected Parameters: outputFileName translationPairsFileName"
	
outputFile = open(outputFileName,'w')

with open(filename,'r') as inputFile: #reading from file and populating the dictionary with their counts one by one
	for line in inputFile:
		line = line.split('\t')
		englishPhrase = line[0].strip()
		foreignPhrase = line[1].strip()
		countDictionary[englishPhrase][foreignPhrase] += 1

writeBuffer = []
for englishPhrase in countDictionary: 
	numberOfForeignPhrases = len(countDictionary[englishPhrase])
	for foreignPhrase in countDictionary[englishPhrase]:
		count = countDictionary[englishPhrase][foreignPhrase]
		probability = count / float(numberOfForeignPhrases)
		writeBuffer.append(englishPhrase+'\t'+foreignPhrase+'\t'+str(probability)+'\n')
		
		
outputFile.write(''.join(writeBuffer))




