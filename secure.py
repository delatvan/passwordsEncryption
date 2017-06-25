import sys
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives import padding

BLOCK_SIZE = 128
Key_SIZE = 256
IV_SIZE = 16

def hashingF(password):
	#Convert simple password into 256 hashKey
	digest = hashes.Hash(hashes.SHA256(),backend=default_backend())
	digest.update(password.encode('UTF-8'))
	key = digest.finalize()
	return key

def paddingF(text,blockSize):
	padder = padding.PKCS7(blockSize).padder()
	paddedData = padder.update(text)+padder.finalize()
	return paddedData

def unpaddingF(text, blockSize):
	unpadder = padding.PKCS7(blockSize).unpadder()
	data = unpadder.update(text)+unpadder.finalize()
	return data

def encryptingF(key, iv, plainText):
	#encrypts a string
	cipher = Cipher(algorithms.AES(key),modes.CBC(iv),
		backend = default_backend())
	encryptor = cipher.encryptor()
	cipher_text = encryptor.update(plainText) + encryptor.finalize()
	return cipher_text

def decryptingF(key, iv, cipherText):
	#decrypts a string
	cipher = Cipher(algorithms.AES(key),modes.CBC(iv),
	backend = default_backend())
	decryptor = cipher.decryptor()
	plaintext = decryptor.update(cipherText) + decryptor.finalize()
	return plaintext

def encryptingFile(fileName, key):
	fileReader = open(fileName,"r")
	firstLine = fileReader.next().split(" ")
	#Case were file hasn't ever been encrypted by this program
	if firstLine[0]!= "decrypted":
		fileWriter = open(fileName+"Encrypted","w")
		fileWriter.write("encrypted file: "+fileName+" \n")
		fileReader.seek(0)
	#Case were file was already encrypted by the program
	else:
		fileWriter = open(firstLine[2]+"Encrypted","w")
		fileWriter.write("encrypted file: "+firstLine[2]+" \n")
	for line in fileReader:
		iv = os.urandom(IV_SIZE)
		cipherText = encryptingF(key,iv,paddingF(line,BLOCK_SIZE))
		fileWriter.write(repr(cipherText)+" "+repr(iv)+" \n")
	fileWriter.flush()
	os.fsync(fileWriter)
	fileWriter.close()
	fileReader.close()
	print "Your file is encrypted"	

def decryptingFile(fileName, key):
	fileReader = open(fileName,"r")	
	firstLine = fileReader.next().split(" ")
	if firstLine[0]!= "encrypted":
		raise ValueError("This file hasn't been encrypted before")
		fileReader.close()
		sys.exit()
	fileWriter = open(firstLine[2]+"Decrypted","w")
	fileWriter.write("decrypted file: "+firstLine[2]+" \n")
	for line in fileReader:
		lineList = line.split(" ")
		cipherText = lineList[0]
		iv = lineList[1] #check
		plaintext = decryptingF(key,iv,cipherText)
		fileWriter.write(unpaddingF(plaintext,BLOCK_SIZE))
	fileWriter.flush()
	os.fsync(fileWriter)
	fileWriter.close()
	fileReader.close()
	print "Your file is decrypted"




# #Get File as argument from the command line
# argList = sys.argv
# try:
# 	fileName = argList[1]
# except Exception, e:
# 	print "No File was given as input"
# 	sys.exit()
# 	pass

# #Open file in reading mode
# fileReader = open(fileName,"r")

# key = hashKey(raw_input("Please enter your encryption or decryption password\n"))


# print "Would you like to decrypt or encrypt your file?"
# userInput = ""
# while userInput!= "x" and userInput!="d" and userInput != "e":
# 	userInput = raw_input("Please type in d or e; x in case you want to close\n").lower()

# if userInput == "d":
	# decryptFile(fileName,fileReader)
# elif userInput == "e":
# 	encryptFile(fileName,fileReader)	
# elif userInput == "x":
# 	print "Goodbye"
# 	fileReader.close()	
# 	sys.exit()

# print "It is highly recommended to delete your input file\n"
# userInput = raw_input("Would you like to remove your input file? Type in Y/N\n").lower()
# if userInput == "y":
# 	os.remove(fileName)


# fileReader.close()


# def closeAll():
# 	#delete any traces and clean memory 
# 	print "bye"
