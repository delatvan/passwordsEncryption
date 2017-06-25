"""delatvan@gmail.com 
	25.06.2017
	"""
import sys
import os
from secure import decryptingFile
from secure import encryptingFile
from secure import hashingF
#Get File as argument from the command line
argList = sys.argv
try:
	fileName = argList[1]
except Exception, e:
	print "No File was given as input"
	sys.exit()
	pass

#Open file in reading mode
fileReader = open(fileName,"r")

pswd = raw_input("Please enter your encryption or decryption password\n")
key = hashingF(pswd)


print "Would you like to decrypt or encrypt your file?"
userInput = ""
while userInput!= "x" and userInput!="d" and userInput != "e":
	userInput = raw_input("Please type in d or e; x in case you want to close\n").lower()

if userInput == "d":
	decryptingFile(fileName,key)
elif userInput == "e":
	encryptingFile(fileName,key)	
elif userInput == "x":
	print "Goodbye"
	fileReader.close()	
	sys.exit()

print "It is highly recommended to delete your input file\n"
userInput = raw_input("Would you like to remove your input file? Type in Y/N\n").lower()
if userInput == "y":
	os.remove(fileName)


fileReader.close()


def closeAll():
	#delete any traces and clean memory 
	print "bye"