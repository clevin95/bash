#!/usr/bin/python
import sys
import os
import re

tokenPairs = os.environ	

def containsDollar (arg):
	while "\\\\" in arg:
		arg = arg.replace("\\\\","``",1)
	while "\$" in arg:
		arg = arg.replace("\$","``",1)
	if "$" in arg:
		return arg.index("$")
	else:
		return None

def getEndIndex (arg):
	while "\\\\" in arg:
		arg = arg.replace("\\\\","``",1)
	while "\{" in arg:
		arg = arg.replace("\{","``",1)
	while "\}" in arg:
		arg = arg.replace("\}","``",1)
	
	bracketCounter = 1
	indexCounter = 0 
	for char in arg:
		if char == '{':
			bracketCounter += 1
		else:
		 if char == '}':
			bracketCounter -= 1
		if bracketCounter == 0:
			return indexCounter;
		indexCounter += 1
	return None

def getEndOfName (arg):
	stringSequence = re.search('\W', arg)
	if stringSequence == None:
		return len(arg)
	else:
		return arg.index(stringSequence.group(0))

def getEndIndexForAnd (arg, startIndex):
	if "$" in arg[startIndex:]:
		endIndex = arg[startIndex:].index("$")
		if "\$" in arg[startIndex:]:
			escapeIndex = arg[startIndex:].index("\$")
			if endIndex == escapeIndex + 1:
				return getEndIndexForAnd(arg, startIndex + endIndex + 1)
			else:
				return endIndex + startIndex
		else:
			return endIndex + startIndex
	else:
		return None

def isValidName (name):
	if "$" in name or " " in name or "}" in name or "{" in name:
		return False
	else:
		return True

def getValueFromArgs (number):
	try:
		arg = sys.argv[number]
		return unpackString(arg)
	except IndexError:
		return ""

def getValueFromPairs (key):
	try:
		return tokenPairs[key]	
	except KeyError:
		return None

def getAllArgs ():
	buildString = ""
	for i in range (1, len(sys.argv)):
		buildString += sys.argv[i]
		buildString += " "
	return unpackString(buildString[:-1])

def expandBracketEnclosed (arg):
	endIndex = getEndIndex(arg[1:])
	if (endIndex is None):
		return None
	else:
		endIndex += 1
	if (ord(arg[1]) < 58 and ord(arg[1]) > 47):
		if (endIndex > 2):
			return None
		number = int(arg[1:endIndex])
		return {"expanded":getValueFromArgs(number),"spanIndex":4}
	sequence = arg[1:endIndex]
	seperateByEqu = sequence.split('=')
	seperateByDash = sequence.split('-')
	if len(seperateByDash) == 1 and len(seperateByEqu) == 1:
		value = getValueFromPairs(sequence)
		if value != None: 
			return {"expanded":getValueFromPairs(sequence),"spanIndex":endIndex + 2}
		return {"expanded":"","spanIndex":endIndex + 2}
	if (len(seperateByDash[0]) < len(seperateByEqu[0])):
		name = seperateByDash[0]
		dashIndex = sequence.index("-") + 1
		word = sequence[dashIndex:endIndex]
		value = getValueFromPairs(name)
		if value != None:
			return {"expanded":value,"spanIndex":endIndex + 2}
			expanded = unpackString(word)
			return {"expanded":expanded,"spanIndex":endIndex + 2}
		return {"expanded":"","spanIndex":endIndex + 2}
	else:
		name = seperateByEqu[0]
		equIndex = sequence.index("=") + 1
		word = sequence[equIndex:endIndex]
		expanded = unpackString(word)
		value = getValueFromPairs(name)
		tokenPairs[name] = unpackString(word)
		if value != none:
			return {"expanded":value,"spanIndex":endIndex +2}
		else:
			return {"expanded":expanded,"spanIndex":endIndex +2}

		

def expand (arg):
	if (len(arg) == 1):
		return {"expanded":arg,"spanIndex":1}
	if (ord(arg[1]) < 58 and ord(arg[1]) > 47):
		endIndex = 1
		number = int(arg[1:2])
		return {"expanded":getValueFromArgs(number),"spanIndex":2}
	if (arg[1] == '{'):
		return expandBracketEnclosed(arg[1:])
	if (arg[1] == '*'):
		return {"expanded":getAllArgs(),"spanIndex":2}
		getAllArgs()
	else:
		endIndex = getEndOfName (arg[1:]) + 1
		expanded = getValueFromPairs(arg[1:endIndex])
		if expanded != None:
			return {"expanded":expanded,"spanIndex":endIndex}
		return {"expanded":"","spanIndex":endIndex}

def unpackString (line):
	line = line.replace('\n','')
	lineBuild = ""
	currentIndex = 0;
	while (currentIndex != len(line)):
		repIndex = containsDollar(line[currentIndex:])
		if  repIndex!= None:
			lineBuild += line[currentIndex:currentIndex + repIndex]
			values = expand(line[currentIndex + repIndex:])
			if values ==  None:
				return None
			currentIndex = currentIndex + repIndex + values["spanIndex"]
			expanded = values["expanded"]
			lineBuild += expanded
		else:
			lineBuild += line[currentIndex:]
			break
	return lineBuild

def test ():
	count = 1
	while(1):
		prompt = "(" + str(count) + ")$ "
		sys.stdout.write(prompt)
		line = sys.stdin.readline()
		if line != '\n':
			if line == '':
				print("")
				break
			lineBuild = unpackString(line)
			if (lineBuild != None):
				print(">> " + lineBuild)
				count += 1
			else:
				sys.stderr.write('Invalid name\n')


test()
