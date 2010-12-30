'''
CMPT 383 (Fall 2010): Final Assignment - Travesty in Python
File: final.py
Naoya Makino
301117541
nmakino@sfu.ca
Dec 3rd, 2010
http://www.cs.sfu.ca/CC/383/ted/383-10-3/Final.html
'''

import sys
import random

class FinalProject:
	def __init__(self, fname):
		self.lemma, self.coll, self.collPoss, self.colPercent = 0, 1, 2, 3
		i = 0
		numOfCol = 8
		lemPoS = 2
		self.adjList, self.nounList, self.adverbList, self.verbList, self.final = [], [], [], [], {}

		corpus = self.getCorpus(fname)
		for line in corpus:
			for word in line:
				if i % numOfCol == lemPoS:
					row = []		
					row.append(line[i-1])
					row.append(line[i+1])
					row.append(line[i+2])
					row.append(0.00) if line[i+5] == '-' else row.append(line[i+5])
					if word == 'j':
						if line[i+2] == 'n':
							self.adjList.append(row)
					if word == 'n':
						self.nounList.append(row)
					if word == 'r':
						self.adverbList.append(row)
					if word == 'v':
						if line[i+2] == 'n' or line[i+2] == 'j':
							self.verbList.append(row)
				i += 1
			i = 0

	def getCorpus(self, fname):
		try:
			f = open(fname)
		except:
			print 'error reading ' + fname
			sys.exit()
		context, words = [], []
		for i, l in enumerate(f):
			if i + 1 >= 41:
				context.append(l)
			pass
		for word in context:
			w = word.split()
			words.append(w)
		return words

	def genSubject(self):
		r = random.randrange(0, len(self.nounList))
		subjectNoun = []
		for noun in self.nounList:
			if noun[self.lemma] == self.nounList[r][self.lemma]:
				subjectNoun.append(noun)
		self.final['subject'] = subjectNoun[0][self.lemma]

	def genVerb(self, typeOfSentence):
		verb = []
		r = random.randrange(0, len(self.verbList))
		for v in self.verbList:
			if v[self.lemma] == self.verbList[r][self.lemma]:
				verb.append(v)
		for v in verb:
			if typeOfSentence == 1:
				if self.genObjectNoun(verb):
					self.final['verb'] = v[self.lemma]
					return True
			else:
				if self.genAdjective(verb):
					self.final['verb'] = v[self.lemma]
					return True
		return False	

	def genObjectNoun(self, verb):
		for v in verb:
			if v[self.collPoss] == 'n':
				if float(v[self.colPercent]) <= 0.5:
					if self.genAdverb(v[self.coll]):
						self.final['objectNoun'] = v[self.coll]
						return True
		return False

	def genAdjective(self, verb):
		for v in verb:
			if v[self.collPoss] == 'j':
				if float( v[self.colPercent]) <= 0.5:
					if self.genObjNounType2(v[self.coll]):
						self.final['adjective'] = v[self.coll]
						return True
		return False

	def genAdverb(self, objNoun):
		nList = []
		for n in self.nounList:
			if n[self.lemma] == objNoun:
				nList.append(n)
		for n in nList:
			if n[self.collPoss] == 'r':
				if float(n[self.colPercent]) <= 0.5:
					self.final['adverb'] = n[self.coll]
					return True
		return False

	def genObjNounType2(self, adj):
		aList = []
		for a in self.adjList:
			if a[self.lemma] == adj:
				aList.append(a)
		for a in aList:
			if a[self.collPoss] == 'n':
				if float(a[self.colPercent]) <= 0.5:
					self.final['objectNounType2'] = a[self.coll]
					return True
		return False

	def genSentence(self, typeOfSentence):
		if typeOfSentence == 1:
			print self.final['subject'][0].upper() + self.final['subject'][1:] + ' ' + self.final['verb'] + ' ' + self.final['objectNoun'] + ' ' +  self.final['adverb'] + '.'
		else:
			print self.final['subject'][0].upper() + self.final['subject'][1:] + ' ' + self.final['verb'] + ' ' + self.final['adjective'] + ' ' +  self.final['objectNounType2'] + '.'

if __name__ == '__main__':
	assert int(sys.argv[2]) > 0
	assert int(sys.argv[3]) == 1 or int(sys.argv[3]) == 2 
	if len(sys.argv) != 4:
		print "Your program should take three command-line arguments. \n" + \
			"The first argument should be the name of the corpus file, \n" + \
			"the second argument should be the number of travesty sentences to generate, \n" + \
			"and the third argument indicates which type of sentence that you should generate\n" + \
			"(a value of '1' specifies Type 1 sentences and '2' specifies Type 2 sentences):" 
		sys.exit()
	else:	
		final = FinalProject(sys.argv[1])
		for i in range(0, int(sys.argv[2])):
			final.genSubject()
			while True:
				if final.genVerb(int(sys.argv[3])):
					final.genSentence(int(sys.argv[3]))
					break

