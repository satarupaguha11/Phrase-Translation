#This file includes implementation of the phrase extraction algorithm

from collections import defaultdict

def extract(fstart, fend, estart, eend, alignmentMatrix, numberOfEnglishWords, numberOfForeignWords, foreignWords, englishWords):
	pair = ''
	if fend==-1:
		return ''
	
	exitFlag = False
	englishPhrase = ''
	foreignPhrase = ''
	#check for consistency from english side
	fdict = defaultdict(int)
	for e in range(estart,eend+1):
		englishPhrase = englishPhrase + englishWords[e]+' '
		for f in range(numberOfForeignWords):
			if alignmentMatrix[e,f] == 1:
				if fstart > f or f > fend:
					exitFlag = True
					break
				else:
					if not fdict.has_key(f):
						foreignPhrase = foreignPhrase + foreignWords[f] + ' '
						fdict[f]=1
		if exitFlag == True:
			englishPhrase = ''
			foreignPhrase = ''
			break

	#check for consistency from foreign side		
	exitFlag1 = False
	englishPhrase1 = ''
	foreignPhrase1 = ''
	e = 0
	
	for f in range(fstart,fend+1):
		foreignPhrase1 = foreignPhrase1 + foreignWords[f]+' '
		for e in range(numberOfEnglishWords):
			if alignmentMatrix[e,f] == 1:
				if estart > e or e > eend:
					exitFlag1 = True
					break
				else:
					englishPhrase1 = englishPhrase1 + englishWords[e] + ' '
		if exitFlag1 == True:
			foreignPhrase = ''
			englishPhrase = ''
			break
	
	if englishPhrase!='' and foreignPhrase!='':
		pair = (englishPhrase,foreignPhrase)
		
	return pair

def extractPhrases(alignmentMatrix,englishSentenceLength,foreignSentenceLength,foreignWords, englishWords,outputFile):
	
	for estart in range(englishSentenceLength): 
		for eend in range(estart,englishSentenceLength):
			numberOfEnglishWords = alignmentMatrix.shape[0]
			numberOfForeignWords = alignmentMatrix.shape[1]
			fstart = foreignSentenceLength - 2
			fend = -1
			for e in range(numberOfEnglishWords):
				for f in range(numberOfForeignWords):
					if alignmentMatrix[e,f] == 1:
						if estart <= e and e <= eend:
							fstart = min(f, fstart)
							fend = max(f, fend)
			ediff = eend - estart
			fdiff = fend - fstart
			if ediff <= 20 and fdiff <= 20: #skipping if phrase length is more than 20
				phrasePair = extract(fstart, fend, estart, eend, alignmentMatrix, numberOfEnglishWords, numberOfForeignWords,foreignWords, englishWords)
				if phrasePair!='':
					outputFile.write(phrasePair[0]+'\t'+phrasePair[1]+'\n') #file phrase pairs to file
			else:
				break
				
			
