
import sys
import os

tokenPairs = os.environ

def getValueFromArgs (number):
	try:
		arg = sys.argv[number]
		return unpackString(arg)
	except ValueError:
		return ""

def getValueFromPairs (key):
	try:
		return tokenPairs[key]	
	except KeyError:
		return ""

def getAllArgs ():
	buildString = ""
	for i in range (1, len(sys.argv)):
		buildString += sys.argv[i]
		buildString += " "
	return unpackString(buildString[:-1])

def expand (arg):
	if (ord(arg[1]) < 58 and ord(arg[1]) > 47):
		endIndex = 1
		number = int(arg[1:2])
		return {"expanded":getValueFromArgs(number),"spanIndex":2}
	if (arg[1] == '{'):
		endIndex = arg.index("}")
		if (ord(arg[2]) < 58 and ord(arg[2]) > 47):
			number = int(arg[2:endIndex])
			return {"expanded":getValueFromArgs(number),"spanIndex":2}
		sequence = arg[2:endIndex]
		seperateByEqu = sequence.split('=')
		seperateByDash = sequence.split('-')
		if (len(seperateByEqu) == 2):
			tokenPairs[seperateByEqu[0]] = seperateByEqu[1]
			expanded = seperateByEqu[1]
		if (len(seperateByDash) == 2):
			expanded = getValueFromPairs(seperateByDash[0])
			if (expanded == ""):
				expanded = unpackString(seperateByDash[1])
		else:
			expanded = getValueFromPairs(sequence)
		return {"expanded":expanded,"spanIndex":endIndex + 1}
	if (arg[1] == '*'):
		return {"expanded":getAllArgs(),"spanIndex":2}
		getAllArgs()
	else:
		endIndex = len(arg)
		if " " in arg:
			endIndex = arg[1:].index(" ") + 1			
		if "$" in arg[1:]:
			endIndex = arg[1:].index("$") + 1
		expanded = getValueFromPairs(arg[1:endIndex])
		return {"expanded":expanded,"spanIndex":endIndex}

def unpackString (line):
	line = line.replace('\n','')
	lineBuild = ""
	currentIndex = 0;
	while (currentIndex != len(line)):
		try:
			repIndex = line[currentIndex:].index("$")
			lineBuild += line[currentIndex:currentIndex + repIndex]
			values = expand(line[currentIndex + repIndex:])
			currentIndex = currentIndex + repIndex + values["spanIndex"]
			expanded = values["expanded"]
			lineBuild += expanded
		except ValueError:
			lineBuild += line[currentIndex:]
			break
	return lineBuild

def test ():
	count = 1
	while(1):
		prompt = "(" + str(count) + ")$ "
		sys.stdout.write(prompt)
		line = sys.stdin.readline()
		lineBuild = unpackString(line)
		print(">> " + lineBuild)
		count += 1

test()
