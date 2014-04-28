----------------------------------------------------------------READ ME------------------------------------------------------------------
1. createAlignmentMatrix.py
   This file takes as input two files generated as output from Giza++. One is the alignment file for English to German translation, while the other is the alignment file for German to English translation.  It also take the path of the output file as argument. This function makes a call to phraseExtraction.py.

   How to run:
   python createAlignmentMatrix.py   path\to\output\file    path\to\alignment\file\english\to\german path\to\alignment\file\german\to\english


2. PhraseExtraction.py
   This module is imported into createAlignmentMatrix.py

3. calculateTranslationProbabilities.py
   This file takes as input the phraseTranslationTable.txt (generated as output when we run the file createAlignmentMatrix.py) as input and generates an output file phraseTranslationProbability.txt(or any other name)

   How to run:
   python calculateTranslationProbabilities.py   path\to\output\file   path\to\input\file

4. stackDecoding.py
   This file takes as input the file phraseTranslationProbability.txt(or any other name, as generated as output from step 3) and a test English sentence. It outputs a translated German sentence. 

   How to run:
   python stackDecoding.py     path\to\input\file   inputsentence
